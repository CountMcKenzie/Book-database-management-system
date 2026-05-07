from tkinter import ttk
import tkinter as tk
import psycopg2

# Creating window and properties

root = tk.Tk()
root.title("RoyalReads Book management System - 100500501")
root.geometry("1500x800")

# Defining page functions

def packViewBooksPage():

    cur.execute("SELECT * FROM BOOK LIMIT 250")

    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    tk.Label(viewFrame, text="Book Inventory Management", font=("Arial", 14, "bold")).pack(pady=5)

    inputFrame = tk.Frame(viewFrame)
    inputFrame.pack(fill="x", padx=20, pady=5)

    tk.Label(inputFrame, text="Book ID:").pack(side="left")
    bookIdEntry = tk.Entry(inputFrame, width=10)
    bookIdEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Publisher:").pack(side="left", padx=(10, 0))
    publisherNameEntry = tk.Entry(inputFrame, width=15)
    publisherNameEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Disc %:").pack(side="left", padx=(10, 0))
    discountPercentEntry = tk.Entry(inputFrame, width=5)
    discountPercentEntry.pack(side="left", padx=5)

    bookTree = ttk.Treeview(viewFrame, columns=("bookID", "title", "price", "categoryID", "publisherID"), show="headings")
    
    bookTree.heading("bookID", text="Book ID")
    bookTree.heading("title", text="Title")
    bookTree.heading("price", text="Retail Price")
    bookTree.heading("categoryID", text="Category ID")
    bookTree.heading("publisherID", text="Publisher ID")

    bookTree.column("bookID", width=80, anchor="center")
    bookTree.column("title", width=250, anchor="w")
    bookTree.column("price", width=100, anchor="e")
    bookTree.column("categoryID", width=100, anchor="center")
    bookTree.column("publisherID", width=100, anchor="center")

    bookTree.pack(fill="both", expand=True, padx=20, pady=10)

    for row in cur.fetchall():
        bookTree.insert("", "end", values=row)

    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    publisherReportBtn = tk.Button(btnFrame, text="Publisher Order Report")
    publisherReportBtn.pack(side="left", padx=5)

    bookHistoryBtn = tk.Button(btnFrame, command=lambda:bookOrderHistoryReportTL(viewFrame), text="View Book History")
    bookHistoryBtn.pack(side="left", padx=5)

    searchBooksBtn = tk.Button(btnFrame, text="Search Books")
    searchBooksBtn.pack(side="left", padx=5)

    applyDiscountBtn = tk.Button(btnFrame, text="Show Discount Results")
    applyDiscountBtn.pack(side="right", padx=5)

def publishersPage():
    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    tk.Label(viewFrame, text="Entity Management (Shops & Publishers)", font=("Arial", 14, "bold")).pack(pady=5)

    cur.execute("SELECT * FROM publisher LIMIT 250")
    publisherRows = cur.fetchall()

    cur.execute("SELECT * FROM shop LIMIT 250")
    shopRows = cur.fetchall()

    # Top Section: Shops
    tk.Label(viewFrame, text="Registered Shops:", font=("Arial", 11, "italic")).pack(pady=(5, 0))
    shopTree = ttk.Treeview(viewFrame, columns=("shopID", "shopName"), show="headings", height=5)
    shopTree.heading("shopID", text="Shop ID")
    shopTree.heading("shopName", text="Shop Name")
    shopTree.column("shopID", width=100, anchor="center")
    shopTree.column("shopName", width=300, anchor="center")
    shopTree.pack(fill="x", padx=20, pady=5)

    for row in shopRows:
        shopTree.insert("", "end", values=row)

    # Bottom Section: Publishers
    tk.Label(viewFrame, text="Registered Publishers:", font=("Arial", 11, "italic")).pack(pady=(10, 0))
    publisherTree = ttk.Treeview(viewFrame, columns=("pubID", "pubName"), show="headings", height=5)
    publisherTree.heading("pubID", text="Publisher ID")
    publisherTree.heading("pubName", text="Publisher Name")
    publisherTree.column("pubID", width=100, anchor="center")
    publisherTree.column("pubName", width=300, anchor="center")
    publisherTree.pack(fill="x", padx=20, pady=5)

    for row in publisherRows:
        publisherTree.insert("", "end", values=row)

    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    addShopBtn = tk.Button(btnFrame, text="Add New Shop")
    addShopBtn.pack(side="left", padx=5)

    addPublisherBtn = tk.Button(btnFrame, text="Add New Publisher")
    addPublisherBtn.pack(side="left", padx=5)

def packOrdersPage():

    def orderRowClick(event):
        selectedItem = shopOrderTree.selection()
        if selectedItem:
            rowData = shopOrderTree.item(selectedItem, "values")
            selectedOrderID, _,_,_,_ = rowData
            cur.execute("""
                SELECT bookid, quantity, unitsellingprice, (unitsellingprice * quantity) AS linetotal 
                FROM orderline 
                WHERE shoporderid = %s
            """, (selectedOrderID,))

            try:
                orderLineTree.delete(*orderLineTree.get_children())
            except tk.TclError:
                pass
            finally:
                for row in cur.fetchall():
                    orderLineTree.insert("","end", values=row)

    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    cur.execute("SELECT * FROM shoporder LIMIT 250")

    tk.Label(viewFrame, text="Order Management", font=("Arial", 14, "bold")).pack(pady=5)

    inputFrame = tk.Frame(viewFrame)
    inputFrame.pack(fill="x", padx=20, pady=5)

    tk.Label(inputFrame, text="Order ID:").pack(side="left")
    shopOrderIdEntry = tk.Entry(inputFrame, width=10, fg="white")
    shopOrderIdEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Book ID:").pack(side="left", padx=(10, 0))
    bookIdEntry = tk.Entry(inputFrame, width=10)
    bookIdEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Qty:").pack(side="left", padx=(10, 0))
    quantityEntry = tk.Entry(inputFrame, width=5, fg="white")
    quantityEntry.pack(side="left", padx=5)

    shopOrderTree = ttk.Treeview(viewFrame, columns=("orderID", "orderDate", "shopID", "repID", "status"), show="headings", height=6)
    
    shopOrderTree.heading("orderID", text="Order ID")
    shopOrderTree.heading("orderDate", text="Date")
    shopOrderTree.heading("shopID", text="Shop ID")
    shopOrderTree.heading("repID", text="Sales Rep")
    shopOrderTree.heading("status", text="Status")

    shopOrderTree.bind("<<TreeviewSelect>>", orderRowClick)

    for col in ("orderID", "orderDate", "shopID", "repID", "status"):
        shopOrderTree.column(col, width=100, anchor="center")

    shopOrderTree.pack(fill="x", padx=20, pady=5)

    for row in cur.fetchall():
        shopOrderTree.insert("", "end", values=row)

    tk.Label(viewFrame, text="Items in Selected Order:", font=("Arial", 14, "bold")).pack(pady=(10, 5))

    orderLineTree = ttk.Treeview(viewFrame, columns=("bookID", "qty", "unitPrice", "lineTotal"), show="headings")
    
    orderLineTree.heading("bookID", text="Book ID")
    orderLineTree.heading("qty", text="Quantity")
    orderLineTree.heading("unitPrice", text="Unit Selling Price")
    orderLineTree.heading("lineTotal", text="Line Total")

    for col in ("bookID", "qty", "unitPrice", "lineTotal"):
        orderLineTree.column(col, width=120, anchor="center")

    orderLineTree.pack(fill="both", expand=True, padx=20, pady=10)

    # --- Button Frame for Transaction Capabilities ---
    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    # Trans 8 & 10: Logic for adding lines to open orders
    addOrderLineBtn = tk.Button(btnFrame, text="Add Book to Order")
    addOrderLineBtn.pack(side="left", padx=5)

    # Search functionality
    searchOrderBtn = tk.Button(btnFrame, text="Search Order")
    searchOrderBtn.pack(side="left", padx=5)

    # Trans 9: Logic for dispatching
    dispatchOrderBtn = tk.Button(btnFrame, text="Mark as Dispatched")
    dispatchOrderBtn.pack(side="right", padx=5)

    return viewFrame

def categoriesPage():

    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    cur.execute("SELECT * FROM category LIMIT 250")

    tk.Label(viewFrame, text="Category Management", font=("Arial", 14, "bold")).pack(pady=5)

    inputFrame = tk.Frame(viewFrame)
    inputFrame.pack(fill="x", padx=20, pady=5)

    tk.Label(inputFrame, text="Cat ID:").pack(side="left")
    catIdEntry = tk.Entry(inputFrame, width=8)
    catIdEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Name:").pack(side="left", padx=(5, 0))
    nameEntry = tk.Entry(inputFrame, width=15)
    nameEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Type:").pack(side="left", padx=(5, 0))
    typeEntry = tk.Entry(inputFrame, width=15)
    typeEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Disc %:").pack(side="left", padx=(10, 0))
    discEntry = tk.Entry(inputFrame, width=5)
    discEntry.pack(side="left", padx=5)


    categoryTree = ttk.Treeview(viewFrame, columns=("ID", "Name", "Type"), show="headings")
    
    categoryTree.heading("ID", text="Category ID")
    categoryTree.heading("Name", text="Name")
    categoryTree.heading("Type", text="Category Type")

    categoryTree.column("ID", width=100, anchor="center")
    categoryTree.column("Name", width=200, anchor="w")
    categoryTree.column("Type", width=150, anchor="w")

    categoryTree.pack(fill="both", expand=True, padx=20, pady=10)

    for row in cur.fetchall():
        categoryTree.insert("","end", values=row)

    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    ttk.Button(btnFrame, command=lambda:addCategoryTL(viewFrame), text="Create New Category").pack(side="left", padx=2)  
    ttk.Button(btnFrame, command=lambda:removeCategoryTL(viewFrame), text="Remove Category").pack(side="left", padx=2)
    ttk.Button(btnFrame, command=lambda:categoryReportTL(viewFrame), text="Category Summary Report").pack(side="left", padx=2)
    ttk.Button(btnFrame, text="Show Discount Results").pack(side="right", padx=2)
    ttk.Button(btnFrame, text="Search/Filter Categories").pack(side="left", padx=2)

    return viewFrame

def staffPage():
    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    cur.execute("SELECT * FROM salesrep LIMIT 250")

    tk.Label(viewFrame, text="Sales Staff Management", font=("Arial", 14, "bold")).pack(pady=5)

    inputFrame = tk.Frame(viewFrame)
    inputFrame.pack(fill="x", padx=20, pady=5)

    tk.Label(inputFrame, text="Rep ID:").pack(side="left")
    salesRepIdEntry = tk.Entry(inputFrame, width=10)
    salesRepIdEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Staff Name:").pack(side="left", padx=(10, 0))
    salesRepNameEntry = tk.Entry(inputFrame, width=20)
    salesRepNameEntry.pack(side="left", padx=5)

    salesRepTree = ttk.Treeview(viewFrame, columns=("repID", "name"), show="headings")
    
    salesRepTree.heading("repID", text="Sales Rep ID")
    salesRepTree.heading("name", text="Full Name")

    salesRepTree.column("repID", width=150, anchor="center")
    salesRepTree.column("name", width=300, anchor="w")

    salesRepTree.pack(fill="both", expand=True, padx=20, pady=10)

    for row in cur.fetchall():
        salesRepTree.insert("", "end", values=row)

    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    addSalesRepBtn = tk.Button(btnFrame, text="Add New Representative")
    addSalesRepBtn.pack(side="left", padx=5)

    removeSalesRepBtn = tk.Button(btnFrame, text="Remove Representative")
    removeSalesRepBtn.pack(side="right", padx=5)

class navButtons:
    def __init__(self, textContent, pageName):
        self.button = ttk.Button(navbar, text=textContent, command= lambda: setPageView(pageName))
    
    def parse(self):
        self.button.pack(side="left", pady=5, padx=5)

# Defining top-level functions

def bookOrderHistoryReportTL(frame):
    orderHistoryWindow = tk.Toplevel(frame)
    orderHistoryWindow.title("Book Order History Report")
    orderHistoryWindow.geometry("1000x650")
    orderHistoryWindow.grab_set()

    tk.Label(orderHistoryWindow, text="Book Order History Report", font=("Arial", 16, "bold")).pack(pady=10)

    searchCriteriaFrame = tk.Frame(orderHistoryWindow)
    searchCriteriaFrame.pack(pady=10)
    
    tk.Label(searchCriteriaFrame, text="Enter Book Identification Number:").pack(side="left", padx=5)
    bookIdentificationEntry = ttk.Entry(searchCriteriaFrame)
    bookIdentificationEntry.pack(side="left", padx=5)

    columnIdentifiers = ("orderDate", "bookTitle", "standardPrice", "unitSellingPrice", "quantity", "totalOrderValue", "shopName")
    orderHistoryTree = ttk.Treeview(orderHistoryWindow, columns=columnIdentifiers, show="headings")
    
    orderHistoryTree.heading("orderDate", text="Order Date")
    orderHistoryTree.heading("bookTitle", text="Book Title")
    orderHistoryTree.heading("standardPrice", text="Retail Price")
    orderHistoryTree.heading("unitSellingPrice", text="Unit Sale Price")
    orderHistoryTree.heading("quantity", text="Quantity")
    orderHistoryTree.heading("totalOrderValue", text="Total Value")
    orderHistoryTree.heading("shopName", text="Shop Name")

    orderHistoryTree.column("orderDate", width=110, anchor="center")
    orderHistoryTree.column("bookTitle", width=200, anchor="w")
    orderHistoryTree.column("standardPrice", width=100, anchor="e")
    orderHistoryTree.column("unitSellingPrice", width=100, anchor="e")
    orderHistoryTree.column("quantity", width=80, anchor="center")
    orderHistoryTree.column("totalOrderValue", width=110, anchor="e")
    orderHistoryTree.column("shopName", width=150, anchor="w")

    orderHistoryTree.pack(fill="both", expand=True, padx=20, pady=5)

    summaryInformationFrame = tk.Frame(orderHistoryWindow, relief="groove", bd=2)
    summaryInformationFrame.pack(fill="x", padx=20, pady=15)
    
    totalCopiesOrderedLabel = tk.Label(summaryInformationFrame, text="Total Copies Ordered: 0", font=("Arial", 10, "bold"))
    totalCopiesOrderedLabel.pack(side="left", padx=20)
    
    totalSellingValueLabel = tk.Label(summaryInformationFrame, text="Total Selling Value: £0.00", font=("Arial", 10, "bold"))
    totalSellingValueLabel.pack(side="right", padx=20)

    def executeReportGeneration():
        targetBook = bookIdentificationEntry.get()
        if not targetBook:
            return

        for existingRow in orderHistoryTree.get_children():
            orderHistoryTree.delete(existingRow)

        try:
            selectionQuery = """
                SELECT 
                    shoporder.orderdate, 
                    book.title, 
                    book.price, 
                    orderline.unitsellingprice, 
                    orderline.quantity, 
                    (orderline.unitsellingprice * orderline.quantity), 
                    shop.name
                FROM book
                JOIN orderline ON book.bookid = orderline.bookid
                JOIN shoporder ON orderline.shoporderid = shoporder.shoporderid
                JOIN shop ON shoporder.shopid = shop.shopid
                WHERE book.bookid = %s
                ORDER BY shoporder.orderdate DESC
            """ 
            cur.execute(selectionQuery, (targetBook,))
            historyResultRows = cur.fetchall()

            for currentRow in historyResultRows:
                # Formatting currency values
                formattedStandardPrice = f"£{currentRow[2]:,.2f}"
                formattedUnitSellingPrice = f"£{currentRow[3]:,.2f}"
                formattedTotalOrderValue = f"£{currentRow[5]:,.2f}"
                
                orderHistoryTree.insert("", tk.END, values=(
                    currentRow[0], 
                    currentRow[1], 
                    formattedStandardPrice, 
                    formattedUnitSellingPrice, 
                    currentRow[4], 
                    formattedTotalOrderValue, 
                    currentRow[6]
                ))

            summaryQuery = """
                SELECT SUM(Quantity), SUM(UnitSellingPrice * Quantity) 
                FROM OrderLine 
                WHERE BookID = %s
            """
            cur.execute(summaryQuery, (targetBook,))
            summaryDataResult = cur.fetchone()
            
            # Extracting values with null handling
            grandTotalCopies = summaryDataResult[0] if summaryDataResult[0] is not None else 0
            grandTotalSellingValue = summaryDataResult[1] if summaryDataResult[1] is not None else 0.0
            
            # Updating summary labels
            totalCopiesOrderedLabel.config(text=f"Total Copies Ordered: {grandTotalCopies}")
            totalSellingValueLabel.config(text=f"Total Selling Value: £{grandTotalSellingValue:,.2f}")

        except Exception as databaseExecutionError:
            connection.rollback()
            print(f"Report Failure: {databaseExecutionError}")

    generateReportButton = ttk.Button(searchCriteriaFrame, text="Generate History", command=executeReportGeneration)
    generateReportButton.pack(side="left", padx=10)

    closeReportButton = tk.Button(orderHistoryWindow, text="Close Report", command=orderHistoryWindow.destroy)
    closeReportButton.pack(pady=10)

def categoryReportTL(frame):
    reportWindow = tk.Toplevel(frame)
    reportWindow.title("Category Summary Report")
    reportWindow.geometry("600x500")

    tk.Label(reportWindow, text="Category Summary Report", font=("Arial", 16, "bold")).pack(pady=10)

    reportTree = ttk.Treeview(reportWindow, columns=("catName", "bookCount", "avgPrice"), show="headings")
    reportTree.heading("catName", text="Category Name")
    reportTree.heading("bookCount", text="Number of Titles")
    reportTree.heading("avgPrice", text="Average Price")

    reportTree.column("catName", width=200, anchor="w")
    reportTree.column("bookCount", width=150, anchor="center")
    reportTree.column("avgPrice", width=150, anchor="e")

    reportTree.pack(fill="both", expand=True, padx=20, pady=5)

    cur.execute("""
        SELECT category.name, COUNT(book.bookid), AVG(book.price)
        FROM category
        LEFT JOIN book ON category.categoryid = book.categoryid
        GROUP BY category.name
        ORDER BY category.name ASC
    """)
    
    reportRows = cur.fetchall()
    for row in reportRows:
        # Format price as currency string
        formattedPrice = f"£{row[2]:,.2f}" if row[2] is not None else "£0.00"
        reportTree.insert("", tk.END, values=(row[0], row[1], formattedPrice))

    # Summary Line Query - Separate query for totals
    cur.execute("SELECT COUNT(bookid), AVG(price) FROM book")
    summaryData = cur.fetchone()
    totalTitles = summaryData[0]
    overallAvg = f"£{summaryData[1]:,.2f}" if summaryData[1] is not None else "£0.00"

    # Summary Frame (Footer)
    summaryFrame = tk.Frame(reportWindow, relief="groove", bd=2)
    summaryFrame.pack(fill="x", padx=20, pady=15)

    tk.Label(summaryFrame, text="TOTALS:", font=("Arial", 10, "bold")).pack(side="left", padx=10)
    tk.Label(summaryFrame, text=f"Total Book Titles: {totalTitles}").pack(side="left", padx=20)
    tk.Label(summaryFrame, text=f"Overall Average Price: {overallAvg}").pack(side="right", padx=20)

    tk.Button(reportWindow, text="Close Report", command=reportWindow.destroy).pack(pady=10)

def addCategoryTL(frame):
    addCategoryWindow = tk.Toplevel(frame)
    addCategoryWindow.title("Create Category")
    addCategoryWindow.geometry("400x350")
    addCategoryWindow.grab_set()

    headerLabel = tk.Label(addCategoryWindow, text="Enter Category Information", font=("Arial", 12, "bold"))
    headerLabel.pack(pady=15)

    categoryIdLabel = tk.Label(addCategoryWindow, text="Category ID:")
    categoryIdLabel.pack()
    categoryIdEntry = ttk.Entry(addCategoryWindow)
    categoryIdEntry.pack(pady=5)

    categoryNameLabel = tk.Label(addCategoryWindow, text="Category Name:")
    categoryNameLabel.pack()
    categoryNameEntry = ttk.Entry(addCategoryWindow)
    categoryNameEntry.pack(pady=5)

    categoryTypeLabel = tk.Label(addCategoryWindow, text="Category Type:")
    categoryTypeLabel.pack()
    categoryTypeEntry = ttk.Entry(addCategoryWindow)
    categoryTypeEntry.pack(pady=5)

    def processCategorySubmission():
        inputCategoryId = categoryIdEntry.get()
        inputCategoryName = categoryNameEntry.get()
        inputCategoryType = categoryTypeEntry.get()

        if inputCategoryType.lower() not in ["fiction", "non-fiction"]:
            return
        
        try:
            cur.execute("INSERT INTO Category (CategoryID, Name, CategoryType) VALUES (%s, %s, %s)", (inputCategoryId, inputCategoryName, inputCategoryType))
            connection.commit()
        except:
            connection.rollback()
            return

        addCategoryWindow.destroy()

    submitButton = ttk.Button(addCategoryWindow, text="Submit Category", command=processCategorySubmission)
    submitButton.pack(pady=25)

def removeCategoryTL(frame):
    removeCategoryWindow = tk.Toplevel(frame)
    removeCategoryWindow.title("Remove Category")
    removeCategoryWindow.geometry("400x250")
    removeCategoryWindow.grab_set()

    headerLabel = tk.Label(removeCategoryWindow, text="Delete Category Record", font=("Arial", 12, "bold"))
    headerLabel.pack(pady=15)

    categoryIdLabel = tk.Label(removeCategoryWindow, text="Enter Category ID to Remove:")
    categoryIdLabel.pack()
    categoryIdEntry = ttk.Entry(removeCategoryWindow)
    categoryIdEntry.pack(pady=5)

    def processCategoryRemoval():
        targetCategoryId = categoryIdEntry.get()

        if not targetCategoryId:
            return

        try:
            removalQuery = "DELETE FROM Category WHERE CategoryID = %s"
            cur.execute(removalQuery, (targetCategoryId,))
            connection.commit()
        except:
            connection.rollback()
            return

        removeCategoryWindow.destroy()

    submitButton = ttk.Button(removeCategoryWindow, text="Remove Record", command=processCategoryRemoval)
    submitButton.pack(pady=25)

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

    viewBooksBtn = navButtons("View Books", "viewBooks").parse()
    viewOrdersBtn = navButtons("View Orders", "vieworders").parse()
    categoriesBtn = navButtons("Categories", "categories").parse()
    staffBtn = navButtons("Staff", "staff").parse()
    publisherBtn = navButtons("Publishers", "publishers").parse()

# Creating tkinter pages

pages = {
    # Ensure keys are kept lower case
    "viewbooks" : packViewBooksPage,
    "vieworders" : packOrdersPage,
    "categories" : categoriesPage,
    "publishers" : publishersPage,
    "staff" : staffPage
}

def setPageView(pageName):
    # Handles logic required to ensure safe page switch
    # pagename -> What page to switch to
    # flushes root -> packs navbar -> packs page below navbar

    flushPage(root)
    packNavBar()
    pages[pageName.lower()]()

# Startup actions 
connection = getDBconnection()
cur = connection.cursor()

setPageView("viewBooks")

# Event loop

root.mainloop()