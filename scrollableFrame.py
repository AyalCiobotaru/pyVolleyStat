import tkinter as tk

class scrollableFrame(tk.Frame):
    """A Tkinter scrollable frame

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, master, *args, **kw):
        tk.Frame.__init__(self, master, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = tk.Scrollbar(self, orient = "vertical")
        self.vscrollbar.pack(fill = "both", side = "right")
        self.canvas = tk.Canvas(self, bd = 0, highlightthickness = 0,
                        yscrollcommand = self.vscrollbar.set)#, bg = "black")
        self.canvas.pack(side = "left", fill = "both", expand = "yes")
        self.vscrollbar.config(command = self.canvas.yview)

        # reset the view
        self.resetView()

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas)#, bg = "pink")
        self.interior_id = self.canvas.create_window(0, 0, window = self.interior,
                                           anchor = "nw")

        self.interior.bind("<Configure>", self.configureInterior)
        self.canvas.bind("<Configure>", self.configureCanvas)

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def configureInterior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion = "0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width = self.interior.winfo_reqwidth())

    def configureCanvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width = self.canvas.winfo_width())

    def getInterior(self):
        return self.interior
    
    def resetView(self):
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
