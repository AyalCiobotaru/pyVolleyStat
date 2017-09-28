import tkinter as tk
from tkinter import messagebox, filedialog
from playerWidget import Player
from scrollableFrame import scrollableFrame
from dataFrameDAO import *
from lastAction import *

class volleyGUI(tk.Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.grid(sticky = "NSEW")

        self.players = ["Ayal","Brendan", "Carl", "James", "Kyle", "Max", "Ryan", "Scott", "Sean", "Tyler", "Yoder"]
        self.playing = []
        self.backgrounds = ["#C2C2C2", "#8A0005"]
        self.foregrounds = ["#8A0005", "#C2C2C2"]
        self.colorTracker = 0
        self.playerWidget = []
        self.columnCount=0
        self.rowCount=0
        self.actions = []

        self.bind("<Configure>", self.onResize)
        self.bind("<Destroy>", self.onExit)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.createMenu()
        self.createVisualCue()

        for x in range(5):
            self.grid_columnconfigure(x, weight = 1)

        for x in range(3):
            self.grid_rowconfigure(x, weight = 1)

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

        self.scframe2 = scrollableFrame(self)

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
            btn = tk.Button(scframe.interior, height = 1, width = 20, relief = "flat",
                bg = "#8A0005", fg = "#E6E6E6",
                font = "Dosis", text = self.players[i],
                command = lambda i = i,x = x: createPlayer(self.players[i]))
            btn.pack(padx = 10, pady = 5, side = "top", fill = "x", expand = "yes")

    def createVisualCue(self):
        self.lastMove = tk.Label(self, text="Select the players in the game",
            width = 52, height = 1,
            relief = "sunken", bg = "#8A0005", fg = "#E6E6E6")
        self.lastMove.grid(row = 2, column = 1, columnspan = 2, ipady = 3, sticky = "NEW")

        self.undoButton = tk.Button(self, text="Undo",
            width = 25, height = 1,
            relief = "raised", bg = "#8A0005", fg = "#E6E6E6",
            command = lambda: self.takeAwayStat(),
            state = "disabled")
        self.undoButton.grid(row = 2, column = 3, sticky = "NEW")

    def updateVisualCue(self, action, add):
        self.undoButton.config(state = "normal")
        self.lastMove.config(text = action.getMessage()) if add else self.lastMove.config(text = action.getRemoveMessage())
        self.updateHistory(action, add)
        if add:
            self.actions.append(action)

    def updateHistory(self, action, add):
        if add:
            self.scframe2.grid(row = 0, column = 4, rowspan = 2, sticky = "NSEW")
            self.colorTracker += 1
            if self.colorTracker == 2:
                self.colorTracker = 0
            txt = tk.Text(self.scframe2.interior, height = 1, width = 25, relief = "flat",
                bg = self.backgrounds[self.colorTracker], fg = self.foregrounds[self.colorTracker],
                font = "Helvitica 10 bold")
            txt.insert("end", action.getMessage()) if add else txt.insert("end", action.getRemoveMessage())
            txt.config(state = "disabled")
            txt.pack(padx = 10, pady = 5, side = "bottom", fill = "x", expand = "yes")
            self.scframe2.resetView()
        else:
            # get's the scrollableFrame object using grid_slaves, then the Frame using getInterior()
            # and finally all the text objects using pack_slaves(), returns a list of text objects
            slaves = self.grid_slaves(0, 4)[0].getInterior().pack_slaves()
            slaves[len(slaves) - 1].pack_forget()

    def takeAwayStat(self):
        try:
            toRemove = self.actions.pop()
            level = toRemove.getLevel()
            sublevel = toRemove.getSublevel()
            player = toRemove.getPlayer()
            removeOneStatDAO(level, sublevel, player)
            if sublevel == "Kill" or sublevel == "Err" or sublevel == "Ace":
                removeOneStatDAO(level, "Att", player) if level == "Attack" else removeOneStatDAO(level, "Tot", player)
                self.toServeAndReceiveButtons()
            else:
                self.toMidPlayButtons()
            self.updateVisualCue(toRemove, False)
        except IndexError:
            messagebox.showerror("Undo",
            "Nothing to Undo")

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
