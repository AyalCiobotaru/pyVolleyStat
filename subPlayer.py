import tkinter as tk

class subPlayer(tk.Toplevel):
    def __init__(self, master, player, title, message, detail):
        tk.Toplevel.__init__(self)
        self.details_expanded = False
        self.title(title)
        self.Master = master
        self.Player = player
        self.geometry("350x75")
        self.minsize(50, 400)
        self.maxsize(425, 500)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0, sticky="nsew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        for i, x in enumerate(self.Master.getPlayers()):
            btn = tk.Button(button_frame, height=1, width=10, relief="flat",
                            bg="#8A0005", fg="#E6E6E6",
                            font="Dosis", text=self.Master.getPlayers()[i],
                            command=lambda i=i, x=x: self.onButtonPress(self.Master.getPlayers()[i]))
            btn.pack(padx=10, pady=5, side="top", fill="x", expand="yes")

    def onButtonPress(self, name):
        self.Player.changeName(name)
        self.destroy()