import requests
import json
from tkinter import *
import urllib.request
from PIL import Image, ImageTk
import sqlite3
import MyLibary
from tkinter import messagebox
import tkinter.ttk as ttk

import MainMenu

def getRespondFromApi(VideoGameName,label): # get information from the api
    API_key = "df1bceb85db049c2b724744f07d31ce4"
    game = VideoGameName.replace(" ", "-")
    response = requests.get(url=f"https://api.rawg.io/api/games/{game}?key={API_key}")
    response = response.json()
    if len(game) > 0:

        if response != {'detail': 'Not found.'}:
            return searchNewGame(response,label)
        else:
            messagebox.showerror(title="Error", message=f"Can't find game named {game}")
    else:
        messagebox.showerror(title="Error", message=f"Empty input")

def searchNewGame(response,label): # Chages information of the labels on the screen

    label["name_label"].configure(text=response["name"])
    label["release_date"].configure(text="Release Date: "+response["released"])
    label["metacritic"].configure(text="Metacritic review: "+ str(response["metacritic"]))
    label["website"].configure(text="Website: "+response["website"])
    label["rating"].configure(text="Average rating: "+str(response["rating"]))
    label["rating_top"].configure(text="Top rating: "+str(response["rating_top"]))
    label["playtime"].configure(text="Playtime: "+str(response["playtime"])+" h")
    label["achievements_count"].configure(text="Achievements count: "+str(response["achievements_count"]))
    label["reddit_url"].configure(text="Reddit: "+response["reddit_url"])
    label["description_raw"].configure(text=response["description_raw"])

    urllib.request.urlretrieve(
        response["background_image"],
        "gfg.png")

    img = Image.open('gfg.png')
    img = img.resize((380,240), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    label["game_image"].configure(image=img)
    label["game_image"].image = img






def add_game(name,user): # add game to the database
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    cursorObj.execute('SELECT videoGame FROM GameCollection WHERE user=? and videoGame=?', (user,name))
    all_rows = cursorObj.fetchall()
    if len(all_rows) > 0:
        messagebox.showerror(title="Error", message=f"{name} is already added to your libary")
    else:
        cursorObj.execute('insert into GameCollection(user,videoGame) values (?,?) ', (user, name))
        conn.commit()
        messagebox.showinfo("Succesful", f"{name} was succesfuly added to your libary")



# Title of the game
def main(response,user):
    changing_label = {}
    display_root = Tk()
    display_root.title("Game Search")
    display_root.geometry("1280x720")
    display_root.config(bg="white")
    display_root.resizable(False, False)
    canvas = Canvas(
        display_root,
        height=680,
        width=440,
    )

    canvas.place(x= 20 , y = 15)


    video_game_title = response["name"]
    #Helvetica
    name_label = Label(display_root, justify="center",text=video_game_title,font=("Arial", 20, 'bold'))
    name_label.place(x= 50 , y = 25, height = 40, width =380)
    changing_label["name_label"] = name_label
    # Show the main image of the game
    urllib.request.urlretrieve(
            response["background_image"],
             "gfg.png")

    img = Image.open('gfg.png')
    img = img.resize((380,240),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    panel = Label(display_root, image=img)
    panel.place(x= 50 , y = 80, height = 240, width =380)
    changing_label["game_image"] = panel



    text_width = 380
    text_height = 30
    text_x = 50
    text_size = 12
    font = "helvetica"

    # Release date
    video_game_release_date = "Release Date: " + response["released"]
    lab = Label(display_root, text=video_game_release_date,anchor='w',font=(font, text_size))
    lab.place(x= text_x , y = 365, height = text_height, width =text_width)
    changing_label["release_date"] = lab
    # Metacritic
    video_game_metacritic = "Metacritic review: " + str(response["metacritic"])
    metacritic_lab = Label(display_root, text=video_game_metacritic,anchor='w',font=(font, text_size))
    metacritic_lab.place(x= text_x , y = 405, height = text_height, width =text_width)
    changing_label["metacritic"] = metacritic_lab
    # Website
    video_game_website = "Website: " + response["website"]
    website_lab = Label(display_root, text=video_game_website,anchor='w',font=(font, text_size))
    website_lab.place(x= text_x , y = 445, height = text_height, width =text_width)
    changing_label["website"] = website_lab
    # Rating
    video_game_rating = "Average rating: " + str(response["rating"])
    rating_lab = Label(display_root, text=video_game_rating,anchor='w',font=(font, text_size))
    rating_lab.place(x=text_x, y=485, height=25, width=text_width)
    changing_label["rating"] = rating_lab
    # Top rating
    video_game_top_rating = "Top rating: " + str(response["rating_top"])
    top_rating_lab = Label(display_root, text=video_game_top_rating,anchor='w',font=(font, text_size))
    top_rating_lab.place(x=text_x, y=525, height=text_height, width=text_width)
    changing_label["rating_top"] = top_rating_lab
    # Playtime
    video_game_playtime = "Playtime: " + str(response["playtime"] )+ " h"
    playtime_lab = Label(display_root, text=video_game_playtime,anchor='w',font=(font, text_size))
    playtime_lab.place(x=text_x, y=565, height=text_height, width=text_width)
    changing_label["playtime"] = playtime_lab
    # achievements_count
    video_game_achievements_count = "Achievements count: " + str(response["achievements_count"])
    achievements_count_lab = Label(display_root, text=video_game_achievements_count,anchor='w',font=(font, text_size))
    achievements_count_lab.place(x=text_x, y=605, height=text_height, width=text_width)
    changing_label["achievements_count"] = achievements_count_lab
    # reddit_url
    video_game_reddit_url = "Reddit: " + response["reddit_url"]
    reddit_url_lab = Label(display_root, text=video_game_reddit_url,anchor='w',font=(font, text_size))
    reddit_url_lab.place(x=text_x, y=645, height=text_height, width=text_width)
    changing_label["reddit_url"] = reddit_url_lab

    reddit_url_lab = Label(display_root, text="Description", anchor='center', font=(font, text_size,"bold"))
    reddit_url_lab.place(x=560, y=150, height=text_height, width=630)

    # Description
    video_game_description = response["description_raw"]
    description_lab = Label(display_root, text=video_game_description, font="helvetica 9",
                        wraplength=630, justify="center",anchor='n',bg="white" )


    description_lab.place(x= 560 , y = 205, height = 500, width =630)
    changing_label["description_raw"] = description_lab
    #Search box




    search_box = ttk.Entry(display_root)
    search_box.place(x= 830 , y = 30, height = 25, width =300)
    search_button = ttk.Button(display_root, text = "Search", command = lambda : [getRespondFromApi(search_box.get(),changing_label)]).place(x = 1140, y = 30)
    add_game_button = ttk.Button(display_root, text="Add game",
                           command=lambda: [add_game(changing_label["name_label"].cget("text"),user)]).place(x=700, y=30)

    # Menu bar

    def exit(root):
        root.destroy()

    def goToLibary(root,user):
        root.destroy()
        MyLibary.main(user)

    def goToMenu(root,user):
        root.destroy()
        MainMenu.main(user)

    # add menu at the top
    menubar = Menu(display_root)
    menubar.config(bg = "white")
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Main Menu", command=lambda: [goToMenu(display_root,user)])
    filemenu.add_command(label="My libary", command=lambda: [goToLibary(display_root,user)])
    filemenu.add_command(label="Exit", command=lambda: exit(display_root))
    filemenu.add_separator()
    menubar.add_cascade(label="Menu", menu=filemenu)
    display_root.config(menu=menubar)
    display_root.mainloop()

