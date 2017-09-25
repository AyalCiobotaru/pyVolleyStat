import tkinter as tk
import pandas as pd
from dataFrameDAO import *

class Player(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        tk.Label(self, text=name, bg = "blue", fg="red").grid(row=0, column=0, columnspan=4)
        self.Name = name
        self.Master = master
        self.initialButtons()
        self.quit = tk.Button(self, bg = "red", text = "X", command = lambda: self.onExit())
        # self.quit.grid(row=0, column=4)

    def midPlayButtons(self):
        self.stat0.config(text="Att", command=lambda: self.buttonCommandHelper("Attack", "Att", self.Name, False))
        self.stat1.config(text="Kill", command=lambda: self.buttonCommandHelper("Attack", "Kill", self.Name, True))
        self.stat2.config(text="Err", command=lambda: self.buttonCommandHelper("Attack", "Err", self.Name, True))
        self.stat3.config(text="Block", command=lambda: self.buttonCommandHelper("Block", "Tot", self.Name, True))
        self.stat4.config(state="normal")
        self.serve1.config(state="disabled")
        self.serve2.config(state="disabled")
        self.serve3.config(state="disabled")

    def showServeRecieve(self):
        self.stat0.config(text="0", command = lambda: self.buttonCommandHelper("Reception", "0", self.Name, False))
        self.stat1.config(text="1", command=lambda: self.buttonCommandHelper("Reception", "1", self.Name, True))
        self.stat2.config(text="2", command=lambda: self.buttonCommandHelper("Reception", "2", self.Name, True))
        self.stat3.config(text="3", command=lambda: self.buttonCommandHelper("Reception", "3", self.Name, True))
        self.stat4.config(state="disabled")
        self.serve1.config(state="normal")
        self.serve2.config(state="normal")
        self.serve3.config(state="normal")

    def buttonCommandHelper(self, level, sublevel, player, changeButtons):
        """Calls addOneStat as well as the midPlayButtons or showServeRecieve functions"""
        self.addOneStat(level, sublevel, player)
        visualCueMessage = self.myStringBuilder(level, sublevel, player)
        self.Master.updateVisualCue(visualCueMessage, level, sublevel, player)
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
        self.stat0 = tk.Button(self, height=2, width=3,
            text = "0", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "0", self.Name, False))
        self.stat0.grid(row=1, column=0, padx=2, pady=2)

        self.stat1 = tk.Button(self, height=2, width=3,
            text = "1", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "1", self.Name, True))
        self.stat1.grid(row=1, column=1, padx=2, pady=2)

        self.stat2 = tk.Button(self, height=2, width=3,
            text = "2", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "2", self.Name, True))
        self.stat2.grid(row=1, column=2, padx=2, pady=2)

        self.stat3 = tk.Button(self, height=2, width=3,
            text = "3", relief = "flat",
            command = lambda: self.buttonCommandHelper("Reception", "3", self.Name, True))
        self.stat3.grid(row=1, column=3, padx=2, pady=2)

        self.stat4 = tk.Button(self, height=2, width=3,
            text = "Dig", relief = "flat",
            command = lambda: self.buttonCommandHelper("Dig", "Tot", self.Name, False),
            state="disabled")
        self.stat4.grid(row=1, column=4, padx=2, pady=2)

        self.serve1 = tk.Button(self, height=1, width = 8,
            text = "Serve", relief = "ridge",
            command = lambda: self.buttonCommandHelper("Serve", "Tot", self.Name, True))
        self.serve1.grid(row=2, column=0, columnspan=2)

        self.serve2 = tk.Button(self, height = 1, width = 8,
            text = "Serve Err", relief = "ridge",
            command = lambda: self.buttonCommandHelper("Serve", "Err", self.Name, False))
        self.serve2.grid(row=2, column=2, columnspan=2)

        self.serve3 = tk.Button(self, height = 1, width = 3,
            text = "Ace", relief = "ridge",
            command = lambda: self.buttonCommandHelper("Serve", "Ace", self.Name, False))
        self.serve3.grid(row=2, column = 4)

    def myStringBuilder(self, level, sublevel, player):
        message = player
        if level == "Attack":
            if sublevel == "Att":
                message += " got an attempt"
            elif sublevel == "Kill":
                message += " got a kill"
            else:
                message += " got a hitting error"
        elif level == "Serve":
            if sublevel == "Tot":
                message += " served the ball in"
            elif sublevel == "Ace":
                message += " got an ace"
            else:
                message += " got a service error"
        elif level == "Dig":
            message += " got a dig"
        elif level == "Block":
            message += " got a block"
        else: # Reception
            if sublevel == "0":
                message += " got aced"
            if sublevel == "1":
                message += " passed a 1"
            if sublevel == "2":
                message += " passed a 2"
            if sublevel == "3":
                message += " passed a 3"
        return message

    def onExit(self):
        print("Hi")
