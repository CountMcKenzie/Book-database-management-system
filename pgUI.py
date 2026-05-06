from tkinter import ttk
import tkinter as tk
import psycopg2

# Creating window and properties

root = tk.Tk()
root.title("RoyalReads Book management System - 100500501")
root.geometry("1500x800")

# Defining page functions

def packViewBooksPage():

    viewFrame = tk.Frame(root)

    infoLabel = tk.Label(viewFrame, text="Book List:", font=("Arial", 14, "bold")).pack(pady=10)

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

def packOrdersPage():

    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    tk.Label(viewFrame, text="Order Tree:", font=("Arial", 14, "bold")).pack(pady=5)

    ordersTree = ttk.Treeview(viewFrame, columns=("ID", "date", "rep", "status"), show="headings")
    
    ordersTree.heading("ID", text="Order ID")
    ordersTree.heading("date", text="Order Date")
    ordersTree.heading("rep", text="Sales Rep")
    ordersTree.heading("status", text="Status")

    # Styling columns
    ordersTree.column("ID", width=100, anchor="center")
    ordersTree.column("date", width=120, anchor="center")
    ordersTree.column("rep", width=150, anchor="w")
    ordersTree.column("status", width=100, anchor="center")

    ordersTree.pack(fill="x", padx=20, pady=5)


    tk.Label(viewFrame, text="Items in Selected Order:", font=("Arial", 14, "bold")).pack(pady=5)

    lineOrderTree = ttk.Treeview(viewFrame, columns=("book", "qty", "retail", "soldAt", "total"), show="headings")
    
    lineOrderTree.heading("book", text="Book Title")
    lineOrderTree.heading("qty", text="Qty")
    lineOrderTree.heading("retail", text="Retail Price")
    lineOrderTree.heading("soldAt", text="Selling Price")
    lineOrderTree.heading("total", text="Line Total")

    lineOrderTree.column("book", width=250, anchor="w")
    lineOrderTree.column("qty", width=50, anchor="center")
    lineOrderTree.column("retail", width=100, anchor="e")
    lineOrderTree.column("soldAt", width=100, anchor="e")
    lineOrderTree.column("total", width=100, anchor="e")

    lineOrderTree.pack(fill="both", expand=True, padx=20, pady=10)

    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    addBookBtn = tk.Button(btnFrame, text="Add Book to Order")
    addBookBtn.pack(side="left")

    dispatchBtn = tk.Button(btnFrame, text="Mark as Dispatched")
    dispatchBtn.pack(side="right")

def categoriesPage():

    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    tk.Label(viewFrame, text="Category Management", font=("Arial", 14, "bold")).pack(pady=5)

    inputFrame = tk.Frame(viewFrame)
    inputFrame.pack(fill="x", padx=20, pady=5)

    tk.Label(inputFrame, text="Cat ID:").pack(side="left")
    catIdEntry = tk.Entry(inputFrame, width=8, bg='white', fg='black')
    catIdEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Name:").pack(side="left", padx=(5, 0))
    nameEntry = tk.Entry(inputFrame, width=15, bg='white', fg='black')
    nameEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Type:").pack(side="left", padx=(5, 0))
    typeEntry = tk.Entry(inputFrame, width=15, bg='white', fg='black')
    typeEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Disc %:").pack(side="left", padx=(10, 0))
    discEntry = tk.Entry(inputFrame, width=5, bg='white', fg='black')
    discEntry.pack(side="left", padx=5)


    categoryTree = ttk.Treeview(viewFrame, columns=("ID", "Name", "Type"), show="headings")
    
    categoryTree.heading("ID", text="Category ID")
    categoryTree.heading("Name", text="Name")
    categoryTree.heading("Type", text="Category Type")

    categoryTree.column("ID", width=100, anchor="center")
    categoryTree.column("Name", width=200, anchor="w")
    categoryTree.column("Type", width=150, anchor="w")

    categoryTree.pack(fill="both", expand=True, padx=20, pady=10)

    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    tk.Button(btnFrame, text="Create New Category").pack(side="left", padx=2)  
    tk.Button(btnFrame, text="Remove Category").pack(side="left", padx=2)
    tk.Button(btnFrame, text="Category Summary Report").pack(side="left", padx=2)
    tk.Button(btnFrame, text="Show Discount Results").pack(side="right", padx=2)
    tk.Button(btnFrame, text="Search/Filter Categories").pack(side="left", padx=2)

    return viewFrame


class navButtons:
    def __init__(self, textContent, pageName):
        self.button = ttk.Button(navbar, text=textContent, command= lambda: setPageView(pageName))
    
    def parse(self):
        self.button.pack(side="left", pady=5, padx=5)

# Defining helper functions

def getDBconnection():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="postgres", # or your specific DB name
            user="postgres",
            password="pass123",
            port=5432
        )
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def flushPage(frame):
    # frame -> Indicates what tkinter frame to clear
    # clears frame specified in input

    for widget in frame.winfo_children():
        widget.destroy()

def packNavBar():
    # Places navbar on screen for user to navigate pages

    global navbar

    navbar = tk.Frame(root, height=50, highlightbackground="white", highlightthickness=1)
    navbar.pack_propagate(False)
    navbar.pack(side="top", fill="x", expand=False)

    homeBtn = navButtons("Home", "home").parse()
    viewBooksBtn = navButtons("View Books", "viewBooks").parse()
    viewOrdersBtn = navButtons("View Orders", "vieworders").parse()
    categoriesBtn = navButtons("Categories", "categories").parse()

# Creating tkinter pages

pages = {
    # Ensure keys are kept lower case
    "viewbooks" : packViewBooksPage,
    "vieworders" : packOrdersPage,
    "categories" : categoriesPage,
}

def setPageView(pageName):
    # Handles logic required to ensure safe page switch
    # pagename -> What page to switch to
    # flushes root -> packs navbar -> packs page below navbar

    flushPage(root)
    packNavBar()
    pages[pageName.lower()]()

# Startup actions 

cur = getDBconnection().cursor()

setPageView("viewBooks")

# Event loop

root.mainloop()