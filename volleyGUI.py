import tkinter as tk
from tkinter import messagebox, filedialog
from playerWidget import Player
from scrollableFrame import scrollableFrame
from dataFrameDAO import *

class Application(tk.Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.grid()
        self.players = ["Ayal","Brendan", "Carl", "James", "Kyle", "Max", "Ryan", "Scott", "Sean", "Tyler", "Yoder"]
        self.playing = []
        self.playerWidget = []
        self.columnCount=0
        self.rowCount=0
        self.bind("<Destroy>", self.onExit)
        self.createMenu()
        self.createBoard()

    def createMenu(self):
        menuBar = tk.Menu(self)
        self.master.config(menu=menuBar)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=self.newSession)
        fileMenu.add_command(label="Save as pickle", command=self.savePickle)
        fileMenu.add_command(label="Save as CSV", command=self.saveCSV)
        fileMenu.add_command(label="Load", command=self.loadSession)
        fileMenu.add_command(label="Exit", command=self.onExit)
        fileMenu.insert_separator(fileMenu.index(tk.END))

    def createBoard(self):
        scframe = scrollableFrame(self.master)
        scframe.grid(row=0,column=0, rowspan=2)

        def createPlayer(player):
            # Check to make sure player isn't already in the game
            if player in self.playing:
                messagebox.showwarning("Add Player",
                "Cannot add %s as he is already in the game" % player)
            else:
                self.columnCount += 1
                newPlayer = Player(self.master, player)
                newPlayer.config(bg="grey", bd=5, relief="raised")
                newPlayer.grid(row=self.rowCount, column=self.columnCount)
                self.playerWidget.append(newPlayer)
                self.playing.append(player)
                # Reset the column count if it gets to 3 to keep it in rows of 3
                if self.columnCount == 3:
                    self.columnCount = 0
                    self.rowCount += 1

        def changeButtons():
            for player in self.playerWidget:
                player.midPlayButtons()
            btn1.config(command=lambda: changeButtonsBack())

        def changeButtonsBack():
            for player in self.playerWidget:
                player.showServeRecieve()
            btn1.config(command=lambda: changeButtons())

        for i, x in enumerate(self.players):
            btn = tk.Button(scframe.interior, height=1, width=20, relief=tk.FLAT,
                bg="gray99", fg="purple3",
                font="Dosis", text=self.players[i],
                command=lambda i=i,x=x: createPlayer(self.players[i]))
            btn.pack(padx=10, pady=5, side=tk.TOP)

        btn1 = tk.Button(self.master, height=1, width=20,
            bg="red", fg="yellow", text="Change",
            command=lambda: changeButtons())
        btn1.grid(row=3,column=0)

    def newSession(self):
        pass

    def loadSession(self):
        pass

    def savePickle(self):
        savedName = filedialog.asksaveasfilename(initialdir ="/Database" ,title = "Select file",filetypes = (("pickle files","*.pickle"),("all files","*.*")), defaultextension=".pickle")
        applyFormulas()
        if savedName is None:
            return
        savePickleDAO(savedName)

    def saveCSV(self):
        savedName = filedialog.asksaveasfilename(initialdir ="/Database" ,title = "Select file",filetypes = (("CSV (Comma delimited)", "*.csv"),("all files","*.*")), defaultextension=".csv")
        applyFormulas()
        if savedName is None:
            return
        saveCSVDAO(savedName)

    def onExit(self, *args, **kw):
        # printDataframe()
        self.quit()
        self.destroy()
