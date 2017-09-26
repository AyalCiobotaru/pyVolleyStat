import tkinter as tk
from tkinter import messagebox, filedialog
from playerWidget import Player
from scrollableFrame import scrollableFrame
from dataFrameDAO import *

class Application(tk.Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.grid(sticky = "NSEW")

        self.players = ["Ayal","Brendan", "Carl", "James", "Kyle", "Max", "Ryan", "Scott", "Sean", "Tyler", "Yoder"]
        self.playing = []
        self.playerWidget = []
        self.columnCount=0
        self.rowCount=0
        self.lastAction = {"level":"", "sublevel":"", "Player":""}

        self.bind("<Configure>", self.onResize)
        self.bind("<Destroy>", self.onExit)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.createMenu()
        self.createVisualCue()

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)

    def onResize(self, event):
         # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height

        # resize the canvas
        self.config(width=self.width, height=self.height)

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
        scframe = scrollableFrame(self)
        scframe.grid(row = 0, column = 0, rowspan = 2, sticky = "NSEW")

        def createPlayer(player):
            # Check to make sure player isn't already in the game
            if player in self.playing:
                messagebox.showwarning("Add Player",
                "Cannot add %s as he is already in the game" % player)

            elif len(self.playing) != 6:
                self.columnCount += 1
                newPlayer = Player(self, player)
                newPlayer.config(bg="grey", bd=5, relief="raised")
                newPlayer.grid(row = self.rowCount, column = self.columnCount, sticky = "NSEW")
                self.playerWidget.append(newPlayer)
                self.playing.append(player)
                # Reset the column count if it gets to 3 to keep it in rows of 3
                if self.columnCount == 3:
                    self.columnCount = 0
                    self.rowCount += 1
            else:
                messagebox.showwarning("Add Player",
                    "Cannot add %s for there are already six players in the game." % player +
                    "\nRemove a player in order to add another." +
                    "\n\nBut that's not implemented yet, so use these guys or start over.")


        for i, x in enumerate(self.players):
            btn = tk.Button(scframe.interior, height=1, width=20, relief=tk.FLAT,
                bg="gray99", fg="purple3",
                font="Dosis", text=self.players[i],
                command=lambda i=i,x=x: createPlayer(self.players[i]))
            btn.pack(padx=10, pady=5, side=tk.TOP)

    def createVisualCue(self):
        self.lastMove = tk.Label(self, text="Select the players in the game",
            width = 52, height = 2,
            relief = "sunken", bg = "black", fg = "white")
        self.lastMove.grid(row = 2, column = 1, columnspan = 2, ipady = 3, sticky = "NSEW")

        self.undoButton = tk.Button(self, text="Undo",
            width = 25, height = 2,
            relief = "raised", bg = "black", fg = "white",
            command = lambda: self.takeAwayStat(),
            state = "disabled")
        self.undoButton.grid(row = 2, column = 3, sticky = "NSEW")

    def updateVisualCue(self, message, level, sublevel, player):
        self.undoButton.config(state = "normal")
        self.lastMove.config(text = message)
        self.lastAction["Player"] = player
        self.lastAction["level"] = level
        self.lastAction["sublevel"] = sublevel

    def takeAwayStat(self):
        removeOneStatDAO(self.lastAction["level"], self.lastAction["sublevel"], self.lastAction["Player"])
        if self.lastAction["sublevel"] == "Kill" or self.lastAction["sublevel"] == "Err" or self.lastAction["sublevel"] == "Ace":
            removeOneStatDAO(self.lastAction["level"], "Att", self.lastAction["Player"]) if self.lastAction["level"] == "Attack" else removeOneStatDAO(self.lastAction["level"], "Tot", self.lastAction["Player"])
        if self.lastAction["level"] == "Serve" or self.lastAction["level"] == "Reception":
            self.toServeAndReceiveButtons()
        else:
            self.toMidPlayButtons()
        self.updateVisualCue("%s's %s stat was removed" % (self.lastAction["Player"], self.lastAction["level"]), "", "" , "")
        self.undoButton.config(state = "disabled")


    def toMidPlayButtons(self):
        for player in self.playerWidget:
            player.midPlayButtons()

    def toServeAndReceiveButtons(self):
        for player in self.playerWidget:
            player.showServeRecieve()

    def newSession(self):
        getEmptyDataFrame()
        messagebox.showinfo("New Database",
        "New empty Database has been loaded.")

    def loadSession(self):
        loadName = filedialog.askopenfile(initialdir = "/Database", title = "Select file", filetypes = (("pickle files","*.pickle"),("all files","*.*")))
        if loadName is None:
            messagebox.showwarning("No Database",
            "No Database has been loaded, please try again.")
        else:
            loadDatabase(loadName)

    def savePickle(self):
        savedName = filedialog.asksaveasfilename(initialdir ="/Database" ,title = "Select file",filetypes = (("pickle files","*.pickle"),("all files","*.*")), defaultextension=".pickle")
        applyFormulas()
        if savedName is "":
            return
        savePickleDAO(savedName)

    def saveCSV(self):
        savedName = filedialog.asksaveasfilename(initialdir ="/Database" ,title = "Select file",filetypes = (("CSV (Comma delimited)", "*.csv"),("all files","*.*")), defaultextension=".csv")
        applyFormulas()
        if savedName is "":
            return
        saveCSVDAO(savedName)

    def onExit(self, *args, **kw):
        # printDataframe()
        self.quit()
        self.destroy()
