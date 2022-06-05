from tkinter import *
import sqlite3
import Login
import uuid
from tkinter import messagebox
from tkinter import ttk

def login(root):
    root.destroy()
    Login.main()

def register(username,password,repassword,root):
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    if password != repassword:
        messagebox.showerror(title="Error", message="Passwords don't match")
    elif len(password) < 8:
        messagebox.showerror(title="Error", message="Passwords should be at least 8 characters long")
    elif len(username) < 8:
        messagebox.showerror(title="Error", message="Username should be at least 8 characters long")
    else:
        if checkIfUserExists(username):
            messagebox.showerror(title="Error", message="The username is already taken")
        else:
            cursorObj.execute('insert into Users(id,Username,Password) values (?,?,?) ', (str(uuid.uuid4()),username,password))
            conn.commit()
            login(root)

def checkIfUserExists(username): # check if our user is in database
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    cursorObj.execute('SELECT * FROM Users WHERE Username=?', (username,))
    all_rows = cursorObj.fetchall()
    if len(all_rows) == 0:
        return False
    return True


def main():
    root = Tk()
    root.title("Login")
    root.geometry("640x360")
    root.config(bg="white")
    # title
    label = Label(root, text="MyVideoGameList",font=("Arial", 35, 'bold'), bg="white",justify="center")
    label.place(x=0, y=30, height=70, width=640)
    # username entry and label
    username_entry = ttk.Entry(root)
    username_entry.place(x=210, y=145, height=25, width=200)
    username_label = Label(root, text="Username", bg="white")
    username_label.place(x=100, y=145, height=25, width=100)
    # password entry and label
    password_entry = ttk.Entry(root, show="*")
    password_entry.place(x=210, y=185, height=25, width=200)
    password_label = Label(root, text="Password", bg="white")
    password_label.place(x=100, y=185, height=25, width=100)
    # repassword entry and label
    repassword_entry = ttk.Entry(root, show="*")
    repassword_entry.place(x=210, y=225, height=25, width=200)
    password_label = Label(root, text="Repeat Password", bg="white")
    password_label.place(x=100, y=225, height=25, width=100)

    login_button = ttk.Button(root, text="Login",
                          command=lambda: login(root)).place(x=200, y=290)

    register_button = ttk.Button(root, text="Register",
                             command=lambda: register(username_entry.get(),password_entry.get(),repassword_entry.get(),root)).place(x=350, y=290)

    root.mainloop()

if __name__=="__main__":
    main()