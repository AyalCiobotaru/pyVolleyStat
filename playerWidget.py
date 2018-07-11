import tkinter as tk
from tkinter import messagebox
from dataFrameDAO import *
from lastAction import *
from subPlayer import subPlayer

class Player(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        self.Label = tk.Label(self, text=name, font = "Helvitica 12 bold", bg = "#C2C2C2", fg="#6B0002")
        self.Label.grid(row = 0, column = 0, columnspan = 5, sticky = "NSEW")
        self.Name = name
        self.Master = master
        self.initialButtons()
        self.quit = tk.Button(self, bg = "#AD0006", fg = "#FFFFFF", text = "sub", width=3,  command = lambda: self.onExit())
        self.quit.grid(row = 0, column = 5, sticky = "NSEW")

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        self.grid_columnconfigure(3, weight = 1)
        self.grid_columnconfigure(4, weight = 1)
        self.grid_columnconfigure(5, weight = 1)

        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)

    def midPlayButtons(self):
        self.stat0.config(text="Att", command=lambda: self.buttonCommandHelper("Attack", "Att", self.Name, False))
        self.stat1.config(text="Kill", command=lambda: self.buttonCommandHelper("Attack", "Kill", self.Name, True))
        self.stat2.config(text="Hitting\nErr", command=lambda: self.buttonCommandHelper("Attack", "Err", self.Name, True))
        self.stat3.config(text="Dig", command=lambda: self.buttonCommandHelper("Dig", "Tot", self.Name, False))
        self.stat4.config(state="normal")
        self.stat5.config(state="normal")
        self.serve1.config(state="disabled")
        self.serve2.config(state="disabled")
        self.serve3.config(state="disabled")

    def showServeRecieve(self):
        self.stat0.config(text="0", command = lambda: self.buttonCommandHelper("Reception", "0", self.Name, False))
        self.stat1.config(text="1", command=lambda: self.buttonCommandHelper("Reception", "1", self.Name, True))
        self.stat2.config(text="2", command=lambda: self.buttonCommandHelper("Reception", "2", self.Name, True))
        self.stat3.config(text="3", command=lambda: self.buttonCommandHelper("Reception", "3", self.Name, True))
        self.stat4.config(state="disabled")
        self.stat5.config(state="disabled")
        self.serve1.config(state="normal")
        self.serve2.config(state="normal")
        self.serve3.config(state="normal")

    def buttonCommandHelper(self, level, sublevel, player, changeButtons):
        """Calls addOneStat as well as the midPlayButtons or showServeRecieve functions"""
        self.addOneStat(level, sublevel, player)
        visualCueMessage = lastAction(level, sublevel, player)
        self.Master.updateVisualCue(visualCueMessage, True)
        if changeButtons:
            if level == "Serve" or level == "Reception":
                self.Master.toMidPlayButtons()
            else:
                self.Master.toServeAndReceiveButtons()

    def addOneStat(self, level, sublevel, player):
        """Calls the addOneStatDAO in order to add one to the desired stat """
        addOneStatDAO(level, sublevel, player)
        # Kill or Error for an attack needs to add one to attempt as well
        # Error or Ace for a serve needs to add one to total as well
        if sublevel == "Kill" or sublevel == "Err" or sublevel == "Ace":
            addOneStatDAO(level, "Att", player) if level == "Attack" else addOneStatDAO(level, "Tot", player)

    def initialButtons(self):
        self.stat0 = tk.Button(self, height = 2, width = 3,
            text = "0", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "0", self.Name, False))
        self.stat0.grid(row = 1, column = 0, padx = 2, pady = 2, sticky = "NSEW")

        self.stat1 = tk.Button(self, height = 2, width = 3,
            text = "1", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "1", self.Name, True))
        self.stat1.grid(row = 1, column = 1, padx = 2, pady = 2, sticky = "NSEW")

        self.stat2 = tk.Button(self, height = 2, width = 3,
            text = "2", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "2", self.Name, True))
        self.stat2.grid(row = 1, column = 2, padx = 2, pady = 2, sticky = "NSEW")

        self.stat3 = tk.Button(self, height = 2, width = 3,
            text = "3", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "3", self.Name, True))
        self.stat3.grid(row = 1, column = 3, padx = 2, pady = 2, sticky = "NSEW")

        self.stat4 = tk.Button(self, height = 2, width = 3,
            text = "Block", relief = "flat",
            command = lambda: self.buttonCommandHelper("Block", "Tot", self.Name, True),
            state="disabled")
        self.stat4.grid(row = 1, column = 4, padx = 2, pady = 2, sticky = "NSEW")

        self.stat5 = tk.Button(self, height = 2, width = 3,
            text = "Block\nErr", relief = "flat",
            command = lambda: self.buttonCommandHelper("Block", "Err", self.Name, True),
            state="disabled")
        self.stat5.grid(row = 1, column = 5, padx = 2, pady = 2, sticky = "NSEW")


        self.serve1 = tk.Button(self, height = 1, width = 7,
            text = "Serve", relief = "ridge",
            command = lambda: self.buttonCommandHelper("Serve", "Tot", self.Name, True))
        self.serve1.grid(row = 2, column = 0, columnspan = 2, sticky = "NSEW")

        self.serve2 = tk.Button(self, height = 1, width = 7,
            text = "Serve Err", relief = "ridge",
            command = lambda: self.buttonCommandHelper("Serve", "Err", self.Name, False))
        self.serve2.grid(row = 2, column = 2, columnspan = 2, sticky = "NSEW")

        self.serve3 = tk.Button(self, height = 1, width = 7,
            text = "Ace", relief = "ridge",
            command = lambda: self.buttonCommandHelper("Serve", "Ace", self.Name, False))
        self.serve3.grid(row = 2, column = 4, columnspan=2, sticky = "NSEW")

    def changeName(self, name):
        if name in self.Master.playing:
            messagebox.showinfo("Already Playing", "%s is already in the game, choose a different player" % name)
        else:
            self.Master.playing.remove(self.Name)
            self.Name = name
            self.Label['text'] = name
            self.Master.playing.append(name)


    def onExit(self):
        dialog = subPlayer(self.master, self, "Choose Player to sub")
        dialog.focus()




        # messagebox.showinfo("Remove Player",
        # "Yea this does nothing yet, but it'll clear this player so you can sub somebody else in but until then, its just a place holder cause it looks weird without it.\n Players %s" % self.Master.getPlayers())
        # for i, x in enumerate(self.Master.getPlayers()):
        #     btn = tk.Button(messagebox, height=1, width=20, relief="flat",
        #                     bg="#8A0005", fg="#E6E6E6",
        #                     font="Dosis", text=self.Master.getPlayers()[i],
        #                     command=lambda i=i, x=x: changeName(self.Master.getPlayers()[i]))
        #     btn.pack(padx=10, pady=5, side="top", fill="x", expand="yes")
