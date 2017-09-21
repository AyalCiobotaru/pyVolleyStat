from volleyGUI import Application
from dataFrameDAO import getEmptyDataFrame
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.title("VolleyStat")
    root.config(bg="gray99")
    getEmptyDataFrame()
    app = Application(master=root)
    app.createBoard()
    app.mainloop()
