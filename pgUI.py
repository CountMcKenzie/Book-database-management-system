from tkinter import ttk
import tkinter as tk

# Creating window and properties

root = tk.Tk()
root.title("RoyalReads Book management System - 100500501")
root.geometry("700x400")

# Defining page functions

def packViewBooksPage():

    viewFrame = tk.Frame(root)

    # Establishing Columns
    bookTree = ttk.Treeview(viewFrame, columns=("BookID", "Title", "Price", "Category"), show="headings")
    bookTree.heading("BookID", text="Book ID")
    bookTree.heading("Title", text="Book Title")
    bookTree.heading("Price", text="Price")
    bookTree.heading("Category", text="Category")

    # Establishing Styles
    bookTree.column("BookID", width=50, anchor="center")
    bookTree.column("Title", width=250, anchor="w") 
    bookTree.column("Price", width=80, anchor="center")
    bookTree.column("Category", width=120, anchor="w")

    bookTree.pack(fill="both", expand=True)
    viewFrame.pack(fill="both", expand=True, side="top")

class navButtons:
    def __init__(self, textContent, pageName):
        self.button = ttk.Button(navbar, text=textContent, command= lambda: setPageView(pageName))
    
    def parse(self):
        self.button.pack(side="left", pady=5, padx=5)

# Defining helper functions

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
    viewBooksBtn = navButtons("View Books", "home").parse()

# Creating tkinter pages
pages = {
    "home" : packViewBooksPage
}

def setPageView(pageName):
    # Handles logic required to ensure safe page switch
    # pagename -> What page to switch to
    # flushes root -> packs navbar -> packs page below navbar

    flushPage(root)
    packNavBar()
    pages[pageName.lower()]()

# Startup actions 

setPageView("home")

# Event loop

root.mainloop()