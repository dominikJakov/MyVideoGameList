from tkinter import *
import sqlite3
import Register
import MainMenu
from tkinter import ttk
from tkinter import messagebox


def login(username,password,root):
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    cursorObj.execute('SELECT * FROM Users WHERE Username=? AND Password=?', (username,password))
    all_rows = cursorObj.fetchall()
    if len(all_rows) != 0:
        root.destroy()
        MainMenu.main(all_rows[0][0])
    else:
        messagebox.showerror(title="Error", message="Invalid password or username")



def register(root):
    root.destroy()
    Register.main()


def sqlSetup(): # setting up tables
    conn = sqlite3.connect('MyVideoGameListDatabase.db')
    c = conn.cursor()

    #CREATE TABLE "GameCollection" ("user"	TEXT,"videoGame"	TEXT,"userScore"	INTEGER,"finished"	INTEGER);
    c.execute("CREATE TABLE IF NOT EXISTS GameCollection (user	TEXT,videoGame	TEXT,userScore	INTEGER,finished	INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS Users (id	TEXT  NOT NULL,Username	TEXT NOT NULL,Password	TEXT NOT NULL,PRIMARY KEY(id))")
    conn.commit()


def main():
    root = Tk()
    root.title("Login")
    root.geometry("640x360")
    root.config(bg="white")
    # Title
    label = Label(root, text="MyVideoGameList",font=("Arial", 35, 'bold'), bg="white",justify="center")
    label.place(x=0, y=30, height=70, width=640)
    # username label and entry
    username_entry = ttk.Entry(root)
    username_entry.place(x=210, y=125, height=25, width=200)
    username_label = Label(root, text="Username",font=("helvetica", 10),bg="white")
    username_label.place(x=100, y=125, height=25, width=100)
    # password label and entry
    password_entry = ttk.Entry(root, show="*")
    password_entry.place(x=210, y=185, height=25, width=200)
    password_label = Label(root, text="Password",font=("helvetica", 10),bg="white")
    password_label.place(x=100, y=185, height=25, width=100)

    # login button
    login_button = ttk.Button(root, text="Login",
                           command=lambda: login(username_entry.get(),password_entry.get(),root)).place(x=200, y=290)

    # register button
    register_button = ttk.Button(root, text="Register",
                           command=lambda: register(root)).place(x=350, y=290)

    root.mainloop()

if __name__ == "__main__":
    sqlSetup() # seeting up tables
    main()