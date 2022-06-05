from tkinter import messagebox
from tkinter import *
import Search
import MyLibary
import Login
import requests
import tkinter.ttk as ttk


def logout(root):
    root.destroy()
    Login.main()

def my_libary(root,user):
    root.destroy()
    MyLibary.main(user)

def CallAPI(VideoGameName,root,win_root): # gets the information from the api
    VideoGameName = VideoGameName.replace(" ", "-")
    API_key = "df1bceb85db049c2b724744f07d31ce4"
    response = requests.get(url=f"https://api.rawg.io/api/games/{VideoGameName}?key={API_key}")
    response = response.json()
    if response != {'detail': 'Not found.'}:
        root.destroy()
    win_root.destroy()
    return response

def callMainScreen(game,root,win_root,user): # calls the main function
    if len(game) > 0:
        response = CallAPI(game, root, win_root)
        if response != {'detail': 'Not found.'}:
            Search.main(response, user)
        else:
            messagebox.showerror(title="Error", message=f"Can't find game named {game}")
    else:
        messagebox.showerror(title="Error", message=f"Empty input")

def search(root,user): # creates as search window
    win_root = Tk()
    win_root.title("Search")
    win_root.geometry("250x150")
    win_root.resizable(False, False)
    win_root.config(bg = "white")
    label = Label(win_root, text="Enter a video game name",font=("Arial", 10, 'bold'), bg="white")
    label.place(x=25, y=10, height=25, width=200)
    game_entry = ttk.Entry(win_root)
    game_entry.place(x=25, y=35, height=25, width=200)
    search_button = ttk.Button(win_root, text="OK", command=lambda: [callMainScreen(game_entry.get(),root,win_root,user)])
    search_button.place(x=90, y=90, height=25, width=70)

def main(user):
    root = Tk()
    root.title("Main Menu")
    root.geometry("640x360")
    root.resizable(False, False)
    root.config(bg = "white")

    label = Label(root, text="MyVideoGameList",font=("Arial", 40, 'bold'), bg="white",justify="center")
    label.place(x=0, y=40, height=70, width=640)

    search_button = ttk.Button(root, text="Search",
                          command=lambda: search(root,user)   ).place(x=280, y=205)

    my_libary_button = ttk.Button(root, text="My Libary",
                          command=lambda: my_libary(root,user)).place(x=430, y=205)

    logout_button = ttk.Button(root, text="Logout",
                              command=lambda: logout(root)).place(x=130, y=205)

    root.mainloop()

if __name__=="__main__":
    main("Admin")