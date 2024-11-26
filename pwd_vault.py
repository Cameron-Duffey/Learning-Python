import sqlite3
import hashlib
import uuid
import pyperclip
import base64
import secrets
import string

from tkinter import *
from tkinter import simpledialog
from functools import partial
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

#Make a key that is randomly generated and will be used to encrypt user data

backend = default_backend()
salt = b'2444'

def kdf():
    return PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=backend)

encryption_key = 0

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(message: bytes, token:bytes) -> bytes:
    return(Fernet(token).decrypt(message))

def gen_password(length: int) -> str:
    return ''.join(
        (
            secrets.choice(string.ascii_letters + string.digits + string.punctuation)
            for i in range(length)
        )
    )

#Database code
with sqlite3.connect('password_vault.db') as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
recovery_key TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterkey(
id INTEGER PRIMARY KEY,
master_key_password TEXT NOT NULL,
master_key_recovery_key TEXT NOT NULL);
""")

#Create popup
def pop_up(text):
    answer = simpledialog.askstring('input string', text)
    return answer

#Create window
window = Tk()
window.update()

window.title('Password Vault')

def hash_password(input):
    hash1 = hashlib.sha256(input)
    hash1 = hash1.hexdigest()

    return hash1

def first_time_screen(has_master_key = None):
    for widget in window.winfo_children():
        widget.destroy()
    
    window.geometry('250x150')

    lbl = Label(window, text='Create a Master Password')
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    lbl1= Label(window, text='Re-enter Password')
    lbl1.pack()
  
    txt1 = Entry(window, width=20, show='*')
    txt1.pack()

    def save_password():
        if txt.get() == txt1.get():
            sql = 'DELETE FROM masterpassword WHERE id = 1'
            cursor.execute(sql)

            hashed_password = hash_password(txt.get().encode())
            key = str(uuid.uuid4().hex)
            hashed_recovery_key = hash_password(key.encode())

            insert_password = """INSERT INTO masterpassword(password, recovery_key)
            VALUES(?, ?)"""
            cursor.execute(insert_password, ((hashed_password), (hashed_recovery_key)))

            #Check if masterkey exists, if it does replace it by encrypting it with new password and new recovery key hash
            #If it does not, generate a masterkey and encrypt it with new password hash, and new recovery key hash
            masterkey = has_master_key if has_master_key else gen_password(64)
            cursor.execute("SELECT * FROM masterkey")
            if cursor.fetchall():
                cursor.execute("DELETE FROM masterkey WHERE id = 1")
            
            insert_masterkey = ("""INSERT INTO masterkey(master_key_password, master_key_recovery_key)
            VALUES(?, ?)""")
            cursor.execute(
                insert_masterkey,
                (
                    (encrypt(masterkey.encode(), base64.urlsafe_b64encode(kdf().derive(txt.get().encode())))),
                    (encrypt(masterkey.encode(), base64.urlsafe_b64encode(kdf().derive(key.encode())))),
                ),
            )

            #Change encryption key to master key uncrypted by masterpasword
            global encryption_key
            encryption_key = base64.urlsafe_b64encode(kdf().derive(masterkey.encode()))

            db.commit()

            recovery_screen(key)
        else:
            lbl.config(text='Passwords do not match')
     
    btn = Button(window, text='Save', command=save_password)
    btn.pack(pady=5)

def recovery_screen(key):
    for widget in window.winfo_children():
        widget.destroy()
    
    window.geometry('250x150')

    lbl = Label(window, text='Save this key to reset password.')
    lbl.config(anchor=CENTER)
    lbl.pack()

    lbl1 = Label(window, text=key)
    lbl1.config(anchor=CENTER)
    lbl1.pack()

    def copy_key():
        pyperclip.copy(lbl1.cget('text'))

    btn = Button(window, text='Copy Key', command=copy_key)
    btn.pack(pady=5)

    def done():
        password_vault()

    btn = Button(window, text='Done', command=done)
    btn.pack(pady=5)

def reset_screen():
    for widget in window.winfo_children():
        widget.destroy()
    
    window.geometry('250x150')

    lbl = Label(window, text='Enter Recovery Key.')
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20)
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.config(anchor=CENTER)
    lbl1.pack()

    def get_recovery_key():
        recovery_key_check = hash_password(str(txt.get()).encode())
        cursor.execute(
            "SELECT * FROM masterpassword WHERE id = 1 AND recovery_key = ?", 
            [(recovery_key_check)],
            )

    def check_recovery_key():
        recover_key = get_recovery_key()

        if recover_key:
            #Unencrypt masterkey and pass it to the first_time_screen
            cursor.execute("SELECT * FROM masterkey")
            master_key_entry = cursor.fetchall()
            if master_key_entry:
                master_key_recovery_key = master_key_entry[0][2]

                master_key = decrypt(master_key_recovery_key, base64.urlsafe_b64encode(kdf().derive(str(txt.get()).encode()))).decode()

                first_time_screen(master_key)
            else:
                print('Master Key entry missing!')
                exit()
        else:
            txt.delete(0, 'end')
            lbl1.config(text='Wrong key')

    btn = Button(window, text='Check Recovery Key', command=check_recovery_key)
    btn.pack(pady=5)

def login_screen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry('200x150')
    lbl = Label(window, text='Enter Master Password')
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.config(anchor=CENTER)
    lbl1.pack(side=TOP)

    def get_master_password():
        check_hashed_password = hash_password(txt.get().encode())

        cursor.execute(
            "SELECT * FROM  masterpassword WHERE id = 1 AND password = ?", 
            [(check_hashed_password)],
            )
        return cursor.fetchall()

    def check_password():
        password = get_master_password()

        if password:
            cursor.execute("SELECT * FROM masterkey")
            master_key_entry = cursor.fetchall()
            if master_key_entry:
                master_key_password = master_key_entry[0][1]
                print(txt.get().encode())
                master_key = decrypt(master_key_password, base64.urlsafe_b64encode(kdf().derive(txt.get().encode())))
                global encryption_key
                encryption_key = base64.urlsafe_b64encode(kdf().derive(master_key))
                password_vault()
            else:
                print('Master Key entry is missing!')
                exit()
        else:
            txt.delete(0, 'end')
            lbl1.config(text='Wrong Password')

    def reset_password():
        reset_screen()

    btn = Button(window, text='Submit', command=check_password)
    btn.pack(pady=5)

    btn = Button(window, text='Reset Password', command=reset_password)
    btn.pack(pady=5)

def password_vault():
    for widget in window.winfo_children():
        widget.destroy()

    def add_entry():
        text1= 'Website'
        text2= 'Username'
        text3= 'Password'

        website= encrypt(pop_up(text1).encode(), encryption_key)
        username= encrypt(pop_up(text2).encode(), encryption_key)
        password= encrypt(pop_up(text3).encode(), encryption_key)

        insert_fields = """INSERT INTO vault(website, username, password)
        VALUES(?,?,?)
        """
        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        password_vault()
    
    def remove_entry(input):
        cursor.execute('DELETE FROM vault WHERE id = ?', (input,))
        db.commit()
        password_vault()
    
    window.geometry('750x750')
    window.resizable(height=None, width=None)
    lbl = Label(window, text='Password Vault')
    lbl.grid(column=1)

    btn = Button(window, text='+', command=add_entry)
    btn.grid(column=1, pady=10)

    lbl1 = Label(window, text='Website')
    lbl1.grid(row=2, column=0, padx=80)
    
    lbl2 = Label(window, text='Username')
    lbl2.grid(row=2, column=1, padx=80)
    
    lbl3 = Label(window, text='Password')
    lbl3.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM vault")
    if cursor.fetchall() != None:
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            if len(array) == 0:
                break

            lbl1 = Label(window, text=decrypt(array[i][1], encryption_key), font=('Helvetica', 12))
            lbl1.grid(row=1+3, column=0)
            
            lbl2 = Label(window, text=decrypt(array[i][2], encryption_key), font=('Helvetica', 12))
            lbl2.grid(row=1+3, column=1)
            
            lbl3 = Label(window, text=decrypt(array[i][3], encryption_key), font=('Helvetica', 12))
            lbl3.grid(row=1+3, column=2)

            btn= Button(window, text='Delete', command=partial(remove_entry, array[i][0]))
            btn.grid(row=i+3, column=3, pady=10)

            i = i+1

            cursor.execute('SELECT * FROM vault')
            if len(cursor.fetchall()) <= i:
                break

cursor.execute("SELECT * from masterpassword")
if cursor.fetchall():
    login_screen()
else:
    first_time_screen()

window.mainloop()