import tkinter as tk
import random
import time


window = tk.Tk()
frame: tk.Frame = None
map:list[list[int]] = None
bombamount:int = None
boardsize: list[int] = None
opencell:list = []
fakeamount = None
day:int = 0
hour:int = 0
minute:int = 0
seconds:int = 0

def clear():
    global frame, map, bombamount, boardsize, opencell, fakeamount, day, hour, minute, seconds
    frame, map, bombamount, boardsize, opencell, fakeamount, day, hour, minute, seconds = None, None, None, None, None, None, 0,0,0,0
def replacewindow():
    global window
    window.destroy()
    window = tk.Tk()
    window.geometry("300x200")
    window.eval('tk::PlaceWindow . center')
    return window


def isWin():
    if bombamount == 0:
        window = replacewindow()
        Label = tk.Label(window, width = 25, text="You Win")
        button = tk.Button(window, width = 25, text = "Play Again", command=start)
        Label.pack()
        button.pack()
        
        

def surrounding(i,j, boardsize, which)-> list:
    global map
    if map[i][j] != 0:
        return []
    retlist = []
    if which:
        if i - 1 > -1:
            retlist.append([i-1,j])
            if j - 1 > -1:
                retlist.append([i-1,j-1])
            if j + 1 < boardsize[0]:
                retlist.append([i-1,j+1])
        if i + 1 < boardsize[0]:
            retlist.append([i+1,j])
            if j - 1 > -1:
                retlist.append([i+1,j-1])
            if j + 1 < boardsize[0]:
                retlist.append([i+1,j+1])
        if j - 1 > -1:
            retlist.append([i,j-1])
        if j + 1 < boardsize[0]:
            retlist.append([i,j+1])
    else:
        if i - 1 > -1:
            retlist.append([i-1,j])
            if j - 1 > -1:
                retlist.append([i-1,j-1])
            if j + 1 < boardsize[1]:
                retlist.append([i-1,j+1])
        if i + 1 < boardsize[0]:
            retlist.append([i+1,j])
            if j - 1 > -1:
                retlist.append([i+1,j-1])
            if j + 1 < boardsize[1]:
                retlist.append([i+1,j+1])
        if j - 1 > -1:
            retlist.append([i,j-1])
        if j + 1 < boardsize[1]:
            retlist.append([i,j+1])
    return retlist

def get_widget_at_grid(parent:tk.Frame, row, col) -> tk.Button:
    for w in parent.winfo_children():
        if w.grid_info().get("row") == row and w.grid_info().get("column") == col:
            return w
    
def findall0(i, j, boardsize, which) -> list:
    global frame, opencell
    visted = [[i,j]]
    bfs_queue = []
    start = [i,j]
    check = surrounding(start[0], start[1], boardsize, which)
    for x in check:
        if x not in opencell:
            bfs_queue.append(x)
    while bfs_queue:
        start = bfs_queue.pop()
        visted.append(start)
        opencell.append(start)
        check = surrounding(start[0],start[1], boardsize, which)
        for x in check:
            if x not in bfs_queue and x not in visted and x not in opencell:
                bfs_queue.append(x)
    for x in visted[1:]:
        widget = get_widget_at_grid(frame, x[0],x[1])
        widget.invoke()
    


def checkGameState(i,j):
    global window, boardsize
    which = boardsize[0] == boardsize[1]
    if map[i][j] == -1:
        window.update()
        time.sleep(1)
        window = replacewindow()
        Label = tk.Label(window, width = 25, text="game over")
        button = tk.Button(window, width = 25, text = "try again", command=start)
        Label.pack()
        button.pack()
    if map[i][j] == 0:
        findall0(i, j, boardsize, which)

def start():
    global window
    clear()
    window = replacewindow()
    play = tk.Button(window, width = 25, text="Easy", command = lambda b = 1: generateMap(b))
    play2 = tk.Button(window, width = 25, text="Medium", command = lambda b = 2: generateMap(b))
    play3 = tk.Button(window, width = 25, text="Hard", command = lambda b = 3: generateMap(b))
    play.pack()
    play2.pack()
    play3.pack()

def r_click(i,j,button: tk.Button, lb: tk.Label):
    global bombamount, fakeamount
    if button['text'] == 'F':
        button.config(text = "")
        if map[i][j] == -1:
            bombamount += 1
        fakeamount += 1
    else:
        button.config(text = "F")
        if map[i][j] == -1:
            bombamount -=1
            isWin()
        fakeamount -=1
    lb.config(text= fakeamount)

def click(i:int,j:int, button: tk.Button):
    global opencell
    if button['text'] != "F":
        global frame
        button.grid_forget()
        text = map[i][j]
        if text == 0:
            text = ""
        label = tk.Label(frame, width = 5, text = text)
        label.grid(row = i, column=j)
        opencell.append([i,j])
        checkGameState(i,j)

def increaseVal(i:int, j:int, map, boardsize, which:bool):
    if which:
        if i - 1 > -1:
            if map[i-1][j] != -1:
                map[i-1][j] += 1
            if j - 1 > -1:
                if map[i-1][j-1] != -1:
                    map[i-1][j-1] += 1
            if j + 1 < boardsize:
                if map[i-1][j+1] != -1:
                    map[i-1][j+1] +=1
        if i + 1 < boardsize:
            if map[i+1][j] != -1:
                map[i+1][j] += 1
            if j - 1 > -1:
                if map[i+1][j-1] != -1:
                    map[i+1][j-1] += 1
            if j + 1 < boardsize:
                if map[i+1][j+1] != -1:
                    map[i+1][j+1] +=1
        if j - 1 > -1:
            if map[i][j-1] != -1:
                map[i][j-1] += 1
        if j + 1 < boardsize:
            if map[i][j+1] != -1:
                map[i][j+1] += 1
    else:
        if i - 1 > -1:
            if map[i-1][j] != -1:
                map[i-1][j] += 1
            if j - 1 > -1:
                if map[i-1][j-1] != -1:
                    map[i-1][j-1] += 1
            if j + 1 < boardsize[1]:
                if map[i-1][j+1] != -1:
                    map[i-1][j+1] +=1
        if i + 1 < boardsize[0]:
            if map[i+1][j] != -1:
                map[i+1][j] += 1
            if j - 1 > -1:
                if map[i+1][j-1] != -1:
                    map[i+1][j-1] += 1
            if j + 1 < boardsize[1]:
                if map[i+1][j+1] != -1:
                    map[i+1][j+1] +=1
        if j - 1 > -1:
            if map[i][j-1] != -1:
                map[i][j-1] += 1
        if j + 1 < boardsize[1]:
            if map[i][j+1] != -1:
                map[i][j+1] += 1

def timer(timelabel:tk.Label):
    global day, hour, minute, seconds
    day2, hour2, minute2, seconds2 = day, hour, minute, seconds
    seconds += 1
    if seconds == 60:
        seconds = 0
        minute += 1
        if minute == 60:
            minute = 0
            hour += 1
            if hour == 24:
                hour = 0
                day += 1
    if day < 10:
        day2 = f'0{day}'
    if hour < 10:
        hour2 = f'0{hour}'
    if minute < 10:
        minute2 = f'0{minute}'
    if seconds < 10:
        seconds2 = f'0{seconds}'
    timelabel.config(text=f'{day2}:{hour2}:{minute2}:{seconds2}')
    timelabel.after(1000, timer, timelabel)


def generateMap(mode: int):
    """_summary_
        Generate the minesweeper board
    Args:
        mode (int): difficult level
        1 = easy
        2 = intermidate
        3 = advance
    """
    global map, bombamount, boardsize, fakeamount
    bomb = 0
    boardsize = 0
    if mode == 1:
        bomb = 10
        boardsize = [9,9]
    elif mode == 2:
        bomb = 40
        boardsize = [16,16]
    else:
        bomb = 99
        boardsize = [30,16]
        
            
    map = [[0 for _ in range(boardsize[1])] for _ in range(boardsize[0])]
    mineset = set()
    which = boardsize[0] == boardsize[1]
    while len(mineset) < bomb:
        if which:
            mineset.add(random.randint(0,boardsize[0]**2 - 1))
        else:
            mineset.add(random.randint(0,479))
    for x in mineset:
        if which:
            i = x // boardsize[0]
            j = x - (i * boardsize[0])
            map[i][j] = -1
            increaseVal(i,j, map, boardsize[0], which)
        else:
            i = x // boardsize[1]
            j = x - (i * boardsize[1])
            map[i][j] = -1
            increaseVal(i,j, map, boardsize, which)
            
    bombamount = len(mineset)
    fakeamount = bombamount
    mineset = None
        
    window = replacewindow()
    w,h = window.maxsize()
    window.geometry(f'{w-10}x{h-45}-1+0')
    global frame
    frame = tk.Frame(window)
    frame2 = tk.Frame(window)
    window.rowconfigure(0, weight= 1)
    window.rowconfigure(1, weight=4)
    window.columnconfigure(0, weight=1)
    frame.grid(row = 1, column= 0, sticky='news')
    frame2.grid(row = 0 , column = 0, sticky='news')
    grid = tk.Frame(frame)
    grid.grid(sticky="news", column=0, row=7)
    frame.rowconfigure(7, weight=1)
    frame.columnconfigure(0, weight=1)
    frame2.rowconfigure(0,weight = 3)
    frame2.columnconfigure(0, weight = 1)
    frame2.columnconfigure(1, weight= 1)
    labelbomb = tk.Label(frame2, width=20, text=bombamount, font = ('Arial', 20))
    labelbomb.grid(column = 1, sticky='news')
    for i in range(boardsize[0]):
        
        for j in range(boardsize[1]):
            button = tk.Button(frame, width=5)
            button.config(command = lambda r = i, c = j, b = button: click(r,c,b))
            button.bind('<Button-3>', lambda _, r = i, c = j, b = button, lb = labelbomb: r_click(r,c,b,lb))
            button.grid(row = i, column = j, sticky='nsew')
    frame.columnconfigure(tuple(range(boardsize[1])), weight=1)
    frame.rowconfigure(tuple(range(boardsize[0])), weight=1)
    #label containing the amount of bombs remaining
    timelabel = tk.Label(frame2, width=20, bg='gray', text = "00:00:00:00", font = ('Arial', 20))
    timelabel.after(1000, timer, timelabel)
    timelabel.grid(row = 0, column= 0, sticky="news")


window.geometry("300x200")
window.eval('tk::PlaceWindow . center')
play = tk.Button(window, width = 25, text="Easy", command = lambda b = 1: generateMap(b))
play2 = tk.Button(window, width = 25, text="Medium", command = lambda b = 2: generateMap(b))
play3 = tk.Button(window, width = 25, text="Hard", command = lambda b = 3: generateMap(b))
play.pack()
play2.pack()
play3.pack()


window.mainloop()
