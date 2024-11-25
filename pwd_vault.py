import sqlite3
import hashlib
from tkinter import *

window = Tk()

window.title('Password Vault')

def firstscreen():
    window.geometry('250x150')

    lbl = Label(window, text='Create Master Password')
    lbl.config(anchor=CENTER)
    lbl.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text='Re-enter Password')
    lbl1.pack()
  
    txt1 = Entry(window, width=20, show='*')
    txt1.pack()

    lbl2 = Label(window)
    lbl2.pack()

    def savePassword():
        if txt.get() == txt1.get():
            pass
        else:
            lbl2.config(text='Passwords do not match!')


    btn = Button(window, text='Save', command=savePassword())
    btn.pack(pady=5)

def loginscreen():
    window.geometry('200x100')
    lbl = Label(window, text='Enter Master Password')
    lbl.config(anchor=CENTER)
    lbl.pack()

    lbl1 = Label(window)
    lbl1.pack()

    txt = Entry(window, width=20, show='*')
    txt.pack()
    txt.focus()

    def checkPassword():
        password = 'test'

        if password == txt.get():
            passwordVault()
        else:
            txt.delete(0,'end')
            lbl1.config(text='Wrong Password')

    btn = Button(window, text='Submit', command=checkPassword)
    btn.pack(pady=5)

def passwordVault():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry('700x350')

    lbl = Label(window, text='Password Vault')
    lbl.config(anchor=CENTER)
    lbl.pack()

firstscreen()
window.mainloop()
