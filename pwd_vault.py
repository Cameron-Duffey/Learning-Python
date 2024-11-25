import sqlite3
import hashlib
from tkinter import *

#Database code
with sqlite3.connect('password_vault.db') as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL)
""")

#Create window
window = Tk()

window.title('Password Vault')

def hash_password(input):
    hash = hashlib.md5(input)
    hash = hash.hexdigest()

    return hash

def first_screen():
    window.geometry('250x150')

    lbl = Label(window, text='Create Master Password')
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    re_lbl= Label(window, text='Re-enter Password')
    re_lbl.pack()
  
    txt1 = Entry(window, width=20, show='*')
    txt1.pack()

    lbl2 = Label(window)
    lbl2.pack()

    def save_password():
        if txt.get() == txt1.get():
            hashed_password = hash_password(txt.get().encode('utf-8'))

            insert_password = """INSERT INTO masterpassword(password)
            VALUES(?)"""
            cursor.execute(insert_password, [(hashed_password)])
            db.commit

            password_vault()
        else:
            lbl2.config(text='Passwords do not match!')


    btn = Button(window, text='Save', command=save_password)
    btn.pack(pady=5)

def login_screen():
    window.geometry('200x100')
    mstr_lbl = Label(window, text='Enter Master Password')
    mstr_lbl.config(anchor=CENTER)
    mstr_lbl.pack()

    lbl3 = Label(window)
    lbl3.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    def get_master_password():
        check_hashed_password = hash_password(txt.get().encode('utf-8'))
        cursor.execute("SELECT = FROM * masterpassword WHERE id = 1 AND password = ?", [(checkHashedPassword)])
        return cursor.fetchall()

    def check_password():
        match = get_master_password()

        if match():
            password_vault()
        else:
            txt.delete(0,'end')
            lbl3.config(text='Wrong Password')

    btn = Button(window, text='Submit', command=check_password)
    btn.pack(pady=5)

def password_vault():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry('700x350')

    pv_lbl = Label(window, text='Password Vault')
    pv_lbl.config(anchor=CENTER)
    pv_lbl.pack()

cursor.execute("SELECT * from masterpassword")
if cursor.fetchall():
    login_screen()
else:
    first_screen()

window.mainloop()
