from tkinter import ttk
import tkinter as tk

# Creating window and properties

root = tk.Tk()
root.title("RoyalReads Book management System - 100500501")
root.geometry("700x400")

# Creating tkinter pages

pages = {
    "home" : "packHomePage()" 
}

class navButtons:
    def __init__(self, textContent, pageName):
        self.button = ttk.Button(navbar, text=textContent, command= lambda: setPageView(pageName))
    
    def parse(self):
        self.button.pack(side="left", pady=5, padx=5)

# Defining Functions

def flushPage(frame):
    # frame -> Indicates what tkinter frame to clear
    # clears frame specified in input

    for widget in frame.winfo_children():
        widget.destroy()

def packNavBar():
    # Places navbar on screen for user to navigate pages

    global navbar

    navbar = tk.Frame(root, bg="#d35e5e", height=50)
    navbar.pack_propagate(False)
    navbar.pack(side="top", fill="x", expand=False)

    homeBtn = navButtons("Home", "home").parse()
    viewBooksBtn = navButtons("View Books", "viewBooks").parse()

def setPageView(pageName):
    # Handles logic required to ensure safe page switch
    # pagename -> What page to switch to
    # flushes root -> packs navbar -> packs page below navbar

    flushPage(root)
    packNavBar()
    #pages(pageName.lower()) # TODO uncomment once pages established

# Startup actions 

setPageView("home")

# Event loop

root.mainloop()