import tkinter as tk
from tkinter import messagebox
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
        self.createBoard()

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


    def onExit(self, *args, **kw):
        # applyFormulas()
        # printDataframe()
        # saveData("test")
        pass
