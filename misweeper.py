from tkinter import *
import random,tkinter.messagebox

root = tkinter.Tk()

root.title("Minesweeper")

row = 10
columns = 10
mines = 10

box = []
buttons = []

colors = ['#FFFFFF', '#0000FF', '#008200', '#008284', '#FF0000', '#840084', '#000084', '#840000',  '#000000']

gameover = False


def create_menu():                      #for creating menubar
    menubar = Menu(root)
    size_menu = Menu(root,tearoff = 0)
    size_menu.add_command(label="small (10x10 with 10 mines)", command=lambda: set_size(10, 10, 10))
    size_menu.add_command(label="medium (20x20 with 80 mines)", command=lambda: set_size(20, 20, 80))
    size_menu.add_command(label="big (25x50 with 200 mines)", command=lambda: set_size(25, 50, 200))

    menubar.add_cascade(label="File",menu=size_menu)
    menubar.add_cascade(label="Exit",command=root.destroy)

    root.config(menu=menubar)

def set_size(r,c,m):                   #for setting window size
    global row, columns, mines
    row = r
    columns = c
    mines = m
    start_Game()

def start_Game():                       #destroys all
    global gameover
    gameover = False
    for x in root.winfo_children():
        if type(x) != tkinter.Menu:
            x.destroy()
    prepare_btn()
    prepareMines()

def prepare_btn():                      #creates and puts all the buttons or boxes
    global row, columns, buttons
    Button(root, text="New Game", command=start_Game).grid(row=0, column=0, columnspan=columns, sticky=N+W+S+E)
    buttons = []
    for x in range(0, row):
        buttons.append([])
        for y in range(0, columns):
            b = Button(root, text=" ", width=2, command=lambda x=x,y=y: OnClick(x,y))
            b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=N+W+S+E)
            buttons[x].append(b)

def prepareMines():                     #assigns mines and numbering to their respective fields
    global row, columns, mines, box
    box = []
    for x in range(0, row):
        box.append([])
        for y in range(0, columns):
            box[x].append(0)

    for _ in range(0, mines):
        # done for preventing two or mines to be in a same place...
        x = random.randint(0, row-1)
        y = random.randint(0, columns-1)

        while box[x][y] == -1:
            x = random.randint(0, row-1)
            y = random.randint(0, columns-1)
        box[x][y] = -1

        if x != 0:
            if y != 0:
                if box[x-1][y-1] != -1:
                    box[x-1][y-1] = int(box[x-1][y-1]) + 1
            if box[x-1][y] != -1:
                box[x-1][y] = int(box[x-1][y]) + 1
            if y != columns-1:
                if box[x-1][y+1] != -1:
                    box[x-1][y+1] = int(box[x-1][y+1]) + 1

        if y != 0:
            if box[x][y-1] != -1:
                box[x][y-1] = int(box[x][y-1]) + 1

        if y != columns-1:
            if box[x][y+1] != -1:
                box[x][y+1] = int(box[x][y+1]) + 1

        if x != row-1:
            if y != 0:
                if box[x+1][y-1] != -1:
                    box[x+1][y-1] = int(box[x+1][y-1]) + 1
            if box[x+1][y] != -1:
                box[x+1][y] = int(box[x+1][y]) + 1
            if y != columns-1:
                if box[x+1][y+1] != -1:
                    box[x+1][y+1] = int(box[x+1][y+1]) + 1


def OnClick(x,y):               # on clicking any button,this function geta called
    global box, buttons, colors, gameover, row, columns
    if gameover:
        return
    buttons[x][y]["text"] = str(box[x][y])
    if box[x][y] == -1:
        buttons[x][y]["text"] = "*"
        buttons[x][y].config(background='red', disabledforeground='black')
        gameover = True
        
        for i in range(0, row):
            for j in range(columns):
                if box[i][j] == -1:
                    buttons[i][j]["text"] = "*"
                    buttons[i][j].config(background='red', disabledforeground='black')
        tkinter.messagebox.showinfo("Game Over", "You have lost.")
    else:
        buttons[x][y].config(disabledforeground=colors[box[x][y]])

    if box[x][y] == 0:
        buttons[x][y]["text"] = " "
        autoClickOn(x,y)
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin()

def autoClickOn(x,y):           #auto opens all the boxes nearby
    global box, buttons, colors, row, columns
    if buttons[x][y]["state"] == "disabled":
        return
    if box[x][y] != 0:
        buttons[x][y]["text"] = str(box[x][y])
    else:
        buttons[x][y]["text"] = " "
    buttons[x][y].config(disabledforeground=colors[box[x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    if box[x][y] == 0:
        if x != 0 and y != 0:
            autoClickOn(x-1,y-1)
        if x != 0:
            autoClickOn(x-1,y)
        if x != 0 and y != columns-1:
            autoClickOn(x-1,y+1)
        if y != 0:
            autoClickOn(x,y-1)
        if y != columns-1:
            autoClickOn(x,y+1)
        if x != row-1 and y != 0:
            autoClickOn(x+1,y-1)
        if x != row-1:
            autoClickOn(x+1,y)
        if x != row-1 and y != columns-1:
            autoClickOn(x+1,y+1)

def onRightClick(x,y):          # on right click the ? sign appears and disappears
    global buttons
    if gameover:
        return
    if buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        buttons[x][y]["text"] = "?"
        buttons[x][y]["state"] = "disabled"
    elif buttons[x][y]["text"] == "?":
        buttons[x][y]["text"] = " "
        buttons[x][y]["state"] = "normal"
    
def checkWin():                 # used for checking if a player wins or not
    global buttons, box, row, columns
    win = True
    for x in range(0, row):
        for y in range(0, columns):
            if box[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        tkinter.messagebox.showinfo("Gave Over", "You have won.")




create_menu()
prepare_btn()
prepareMines()
root.mainloop()
