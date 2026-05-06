import tkinter as tk

# Creating window and properties

root = tk.Tk()
root.title("RoyalReads Book management System - 100500501")
root.geometry("700x400")

# Adding widgets

label = tk.Label(root, text="Hello World!")
label.pack() 

# event loop

root.mainloop()