from volleyGUI import volleyGUI
from dataFrameDAO import getEmptyDataFrame
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.title("VolleyStat")
    root.config(bg="gray99")
    root.grid_columnconfigure(0, weight = 1)
    root.grid_rowconfigure(0, weight = 1)
    getEmptyDataFrame()
    app = volleyGUI(master=root)
    app.createBoard()
    app.mainloop()
