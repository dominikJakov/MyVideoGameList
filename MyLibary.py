from tkinter import *

import requests
import sqlite3
import MainMenu
import Search
from tkinter import ttk
from tkinter import messagebox

def showSelected(root,user,listbox): # search the select game
    curItem = listbox.focus()
    if listbox.item(curItem)['values'] == '':
        return
    game = listbox.item(curItem)['values'][1].replace(" ","-")
    root.destroy()
    VideoGameName = game.replace(" ", "-")
    API_key = "df1bceb85db049c2b724744f07d31ce4"
    response = requests.get(url=f"https://api.rawg.io/api/games/{VideoGameName}?key={API_key}")
    response = response.json()
    Search.main(response,user)

def deleteGame(root,user,listbox): # delete the selected game
    curItem = listbox.focus()
    if listbox.item(curItem)['values'] == '':
        return
    game = listbox.item(curItem)['values'][1]
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    cursorObj.execute('delete from GameCollection where videoGame=? and user=?', (game,user))
    conn.commit()
    fillListBox(listbox,user)

def getIndexFromListbox(listbox): # get the index of the game
    curItem = listbox.focus()
    index = listbox.item(curItem)['values'][0]
    return index


def addScore(user,listbox): # Pop up window for us to type the score
    curItem = listbox.focus()
    if listbox.item(curItem)['values'] == '':
        return
    win_root = Tk()
    win_root.title("Search")
    win_root.config(bg="white")
    win_root.geometry("250x150")
    win_root.resizable(False, False)
    label = Label(win_root, text="Add Score",bg="white",justify="center")
    label.place(x=0, y=10, height=25, width=250)
    game_entry = ttk.Entry(win_root)
    game_entry.place(x=30, y=35, height=25, width=200)
    add_button = ttk.Button(win_root, text="OK", command=lambda: [putScoreDatabase(user,game_entry.get(),listbox),win_root.destroy()])
    add_button.place(x=90, y=90, height=25, width=70)


def addProc(user,listbox): # pop up window for us to type the played section
    curItem = listbox.focus()
    if listbox.item(curItem)['values'] == '':
        return
    win_root = Tk()
    win_root.title("Search")
    win_root.geometry("250x150")
    win_root.config(bg="white")
    win_root.resizable(False, False)
    label = Label(win_root, text="Add how much did you finish",bg="white",justify="center")
    label.place(x=0, y=10, height=25, width=250)
    game_entry = ttk.Entry(win_root)
    game_entry.place(x=30, y=35, height=25, width=200)
    add_button = Button(win_root, text="OK", command=lambda: [putProc(user,game_entry.get(),listbox),win_root.destroy()])
    add_button.place(x=90, y=90, height=25, width=70)

def putProc(user,score,listbox): # error checking and adding the value
    if len(score) == 0 :
        messagebox.showerror(title="Error", message="Input can't be empty")
        return
    elif not (score.isnumeric()) :
        messagebox.showerror(title="Error", message="Input has to be only numbers")
        return
    elif int(score) > 100 or int(score) < 0:
        messagebox.showerror(title="Error", message="Input can be only from 0 - 100")
        return
    curItem = listbox.focus()
    game = listbox.item(curItem)['values'][1]
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    cursorObj.execute('UPDATE GameCollection set finished=? where videoGame=? and user=?', (score,game,user))
    conn.commit()
    fillListBox(listbox,user)

def putScoreDatabase(user,score,listbox): # error checking and adding the value
    curItem = listbox.focus()
    game = listbox.item(curItem)['values'][1]
    if len(score) == 0 :
        messagebox.showerror(title="Error", message="Input can't be empty")
        return
    elif not (score.isnumeric()):
        messagebox.showerror(title="Error", message="Input has to be only numbers")
        return
    elif int(score) > 100 or int(score) < 0:
        messagebox.showerror(title="Error", message="Input can be only from 0 - 100")
        return
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    cursorObj.execute('UPDATE GameCollection set userScore=? where videoGame=? and user=?', (score,game,user))
    conn.commit()
    fillListBox(listbox,user)


def findUserGames(user): # find the users games
    conn = sqlite3.connect("MyVideoGameListDatabase.db")
    cursorObj = conn.cursor()
    cursorObj.execute('SELECT videoGame,userScore,finished FROM GameCollection WHERE user=?', (user,))
    all_rows = cursorObj.fetchall()
    return all_rows

def fillListBox(listbox,user): # refresh the list
    for i in listbox.get_children():
        listbox.delete(i)
    user_games = findUserGames(user)
    user_games = insertionSort(user_games)
    for i in range(len(user_games)):
        proc = str(user_games[i][2])
        if proc == "None":
            proc = "0"
        listbox.insert('', 'end', text=str(i), values=(str(i), user_games[i][0], str(user_games[i][1]), proc+" %"))

def insertionSort(array): # insertion sorting algoritam
    sorting_array = []
    unsorting_array = []
    for i in range(len(array)):
        if array[i][1] != None:
            sorting_array.append(array[i])
        else:
            unsorting_array.append(array[i])

    for step in range(1, len(sorting_array)):
        key = sorting_array[step]
        j = step - 1

        while j >= 0 and key[1] > sorting_array[j][1]:
            sorting_array[j + 1] = sorting_array[j]
            j = j - 1

        sorting_array[j + 1] = key
    for tuple in unsorting_array:
        sorting_array.append(tuple)
    return sorting_array


def main(user):
    # create the window
    root = Tk()
    root.title("Main Menu")
    root.geometry("640x360")
    root.resizable(False, False)
    root.config(bg = "white")
    s = ttk.Style()
    s.theme_use('clam')

    # Add a Treeview widget
    tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4"), show='headings', height=5 )
    tree.bind('<Motion>', 'break')
    tree.heading("c1", text="Index")
    tree.column("c1", minwidth=0, width=99, stretch=NO,anchor="center")
    tree.heading("c2", text="Name")
    tree.column("c2", minwidth=0, width=275, stretch=NO,anchor="center")
    tree.heading("c3", text="Score")
    tree.column("c3", minwidth=0, width=117, stretch=NO,anchor="center")
    tree.heading("c4", text="Played")
    tree.column("c4", minwidth=0, width=117, stretch=NO,anchor="center")
    # Define a label for the list.
    label = Label(root, text="My List",justify="center",bg="white",font=("Arial", 14, 'bold'))
    # add the scrollingbar for the list
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    tree.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=tree.yview)
    fillListBox(tree,user)

    select_button = ttk.Button(root, text="Search",
                          command=lambda: showSelected(root,user,tree)).place(x=107, y=305)

    delete_button = ttk.Button(root, text="Delete",
                          command=lambda: deleteGame(root,user,tree)).place(x=213, y=305)

    add_score_button = ttk.Button(root, text="Add score",
                          command=lambda: addScore(user,tree)).place(x=320, y=305)

    proc_button = ttk.Button(root, text="Played",
                              command=lambda: addProc(user, tree)).place(x=427, y=305)


    tree.place(x=5, y=40, height=240, width=610)
    label.place(x=0, y=10, height=25, width=640)


    def goToMainMenu(root,user):
        root.destroy()
        MainMenu.main(user)


    # add a menu bar at the top
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Main Menu", command=lambda: [goToMainMenu(root,user)])
    filemenu.add_separator()
    menubar.add_cascade(label="Menu", menu=filemenu)
    root.config(menu=menubar)

    root.mainloop()


if __name__ == "__main__":
    main("Admin")