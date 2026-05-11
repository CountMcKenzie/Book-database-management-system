from tkinter import ttk
import tkinter as tk
import psycopg2
import json

# Creating window and properties

root = tk.Tk()
root.title("RoyalReads Book management System - 100500501")
root.geometry("1500x800")

# Defining page functions

def packViewBooksPage():

    cur.execute("SELECT * FROM BOOK LIMIT 250")

    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    tk.Label(viewFrame, text="Book Inventory Management", font=("Arial", 15)).pack(pady=5)

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

    bookHistoryBtn = tk.Button(btnFrame, command=lambda:bookOrderHistoryReportTL(viewFrame), text="View Book History")
    bookHistoryBtn.pack(side="left", padx=5)

def shopAndPublishersPage():
    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    tk.Label(viewFrame, text="Shops & Publishers", font=("Arial", 15)).pack(pady=5)

    cur.execute("SELECT * FROM publisher LIMIT 250")
    publisherRows = cur.fetchall()

    cur.execute("SELECT * FROM shop LIMIT 250")
    shopRows = cur.fetchall()

    # Top Section: Shops
    tk.Label(viewFrame, text="Registered Shops:", font=("Arial", 16)).pack(pady=(5, 0))
    shopTree = ttk.Treeview(viewFrame, columns=("shopID", "shopName"), show="headings", height=5)
    shopTree.heading("shopID", text="Shop ID")
    shopTree.heading("shopName", text="Shop Name")
    shopTree.column("shopID", width=100, anchor="center")
    shopTree.column("shopName", width=300, anchor="center")
    shopTree.pack(fill="x", padx=20, pady=5)

    for row in shopRows:
        shopTree.insert("", "end", values=row)

    # Bottom Section: Publishers
    tk.Label(viewFrame, text="Registered Publishers:", font=("Arial", 16)).pack(pady=(10, 0))
    publisherTree = ttk.Treeview(viewFrame, columns=("pubID", "pubName"), show="headings", height=5)
    publisherTree.heading("pubID", text="Publisher ID")
    publisherTree.heading("pubName", text="Publisher Name")
    publisherTree.column("pubID", width=100, anchor="center")
    publisherTree.column("pubName", width=300, anchor="center")
    publisherTree.pack(fill="x", padx=20, pady=5)

    for row in publisherRows:
        publisherTree.insert("", "end", values=row)

    # Button Frame

    bttnFrame = tk.Frame(viewFrame).pack(fill="x", padx=20, pady=10)

    tk.Button(bttnFrame, text="Publisher Report", command=lambda:publisherReportTL(bttnFrame)).pack(side="left", padx=5, pady=10)

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

    tk.Label(viewFrame, text="Order Management", font=("Arial", 16)).pack(pady=5)

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
        shopOrderTree.insert("", "end", values=(row[0], row[1], row[2], row[3], "Open" if row[4] is None else row[4]))

    tk.Label(viewFrame, text="Items in Selected Order:", font=("Arial", 16)).pack(pady=(10, 5))

    orderLineTree = ttk.Treeview(viewFrame, columns=("bookID", "qty", "unitPrice", "lineTotal"), show="headings")
    
    orderLineTree.heading("bookID", text="Book ID")
    orderLineTree.heading("qty", text="Quantity")
    orderLineTree.heading("unitPrice", text="Unit Selling Price")
    orderLineTree.heading("lineTotal", text="Line Total")

    for col in ("bookID", "qty", "unitPrice", "lineTotal"):
        orderLineTree.column(col, width=120, anchor="center")

    orderLineTree.pack(fill="both", expand=True, padx=20, pady=10)

    btnFrame = tk.Frame(viewFrame)
    btnFrame.pack(fill="x", padx=20, pady=10)

    addOrderLineBtn = tk.Button(btnFrame, command=lambda:addOrderLineTL(viewFrame), text="Add Book to Order")
    addOrderLineBtn.pack(side="left", padx=5)

    dispatchOrderBtn = tk.Button(btnFrame, command=lambda:dispatchOrderTL(viewFrame), text="Mark as Dispatched")
    dispatchOrderBtn.pack(side="right", padx=5)

    return viewFrame

def categoriesPage():

    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    cur.execute("SELECT * FROM category LIMIT 250")

    tk.Label(viewFrame, text="Category Management", font=("Arial", 16)).pack(pady=5)

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
    ttk.Button(btnFrame, command=lambda:categoryDiscountReportTL(viewFrame), text="Show Discount Report").pack(side="left", padx=2)

    return viewFrame

def staffPage():
    viewFrame = tk.Frame(root)
    viewFrame.pack(fill="both", expand=True)

    cur.execute("SELECT * FROM salesrep LIMIT 250")

    tk.Label(viewFrame, text="Sales Staff Management", font=("Arial", 16)).pack(pady=5)

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

    repReportBtn = ttk.Button(btnFrame, command=lambda:generateSalesReportTL(viewFrame), text="Generate Rep Report")
    repReportBtn.pack(side="left", padx=5)

class navButtons:
    def __init__(self, textContent, pageName):
        self.button = ttk.Button(navbar, text=textContent, command= lambda: setPageView(pageName))
    
    def parse(self):
        self.button.pack(side="left", pady=5, padx=5)

# Defining top level functions

def publisherReportTL(frame):
    reportWindow = tk.Toplevel(frame)
    reportWindow.title("Publisher Sales Report")
    reportWindow.geometry("950x600")

    tk.Label(reportWindow, text="Monthly Sales Report by Publisher", font=("Arial", 12)).pack(pady=15)

    inputFrame = tk.Frame(reportWindow)
    inputFrame.pack(pady=5)

    tk.Label(inputFrame, text="Enter Publisher Name:").pack(side="left", padx=5)
    pubNameEntry = ttk.Entry(inputFrame, width=30)
    pubNameEntry.pack(side="left", padx=5)

    cols = ("year", "month", "bookid", "title", "numOrders", "totalQty", "orderValue", "retailValue")
    reportTree = ttk.Treeview(reportWindow, columns=cols, show="headings")
    
    reportTree.heading("year", text="Year")
    reportTree.heading("month", text="Month")
    reportTree.heading("bookid", text="Book ID")
    reportTree.heading("title", text="Title")
    reportTree.heading("numOrders", text="Orders")
    reportTree.heading("totalQty", text="Total Qty")
    reportTree.heading("orderValue", text="Order Val (£)")
    reportTree.heading("retailValue", text="Retail Val (£)")

    for col in cols:
        reportTree.column(col, width=90, anchor="center")
    reportTree.column("title", width=200, anchor="w")
    
    reportTree.pack(fill="both", expand=True, padx=20, pady=10)

    def executeReportQuery():
        inputPubName = pubNameEntry.get()
        if not inputPubName:
            return

        # Clear existing data
        reportTree.delete(*reportTree.get_children())

        try:
            query = """
            WITH OrderDetails AS (
                SELECT 
                    EXTRACT(YEAR FROM shoporder.orderdate) AS order_year,
                    EXTRACT(MONTH FROM shoporder.orderdate) AS order_month,
                    book.bookid,
                    book.title,
                    book.price AS list_price,
                    orderline.quantity,
                    orderline.unitsellingprice,
                    orderline.shoporderid
                FROM publisher
                JOIN book ON publisher.publisherid = book.publisherid
                JOIN orderline ON book.bookid = orderline.bookid
                JOIN shoporder ON orderline.shoporderid = shoporder.shoporderid
                WHERE publisher.name = %s
            )
            SELECT 
                order_year,
                order_month,
                bookid,
                title,
                COUNT(shoporderid) AS total_orders,
                SUM(quantity) AS total_quantity_sold,
                SUM(quantity * unitsellingprice) AS actual_revenue,
                SUM(quantity * list_price) AS potential_revenue
            FROM OrderDetails
            GROUP BY 
                order_year, 
                order_month, 
                bookid, 
                title
            ORDER BY 
                order_year DESC, 
                order_month DESC, 
                title ASC;
            """
            cur.execute(query, (inputPubName,))
            reportRows = cur.fetchall()

            for row in reportRows:
                displayData = (
                    int(row[0]), 
                    int(row[1]), 
                    row[2], 
                    row[3], 
                    row[4], 
                    row[5], 
                    f"£{row[6]:,.2f}", 
                    f"£{row[7]:,.2f}"
                )
                reportTree.insert("", tk.END, values=displayData)

            if not reportRows:
                print(f"No records found for Publisher: {inputPubName}")

        except Exception as dbError:
            print(f"Database Error during report generation: {dbError}")

    submitButton = ttk.Button(inputFrame, text="Generate Report", command=executeReportQuery)
    submitButton.pack(side="left", padx=10)

    closeButton = ttk.Button(reportWindow, text="Close", command=reportWindow.destroy)
    closeButton.pack(pady=10)

def dispatchOrderTL(frame):
    dispatchWindow = tk.Toplevel(frame)
    dispatchWindow.title("Update Order Status")
    dispatchWindow.geometry("400x250")
    dispatchWindow.grab_set()

    tk.Label(dispatchWindow, text="Dispatch Order Management", font=("Arial", 16)).pack(pady=15)

    tk.Label(dispatchWindow, text="Enter Order ID to Dispatch:").pack()
    orderIdEntry = ttk.Entry(dispatchWindow)
    orderIdEntry.pack(pady=5)

    def executeDispatchUpdate():
        inputOrderId = orderIdEntry.get()
        if not inputOrderId:
            return

        try:
            query = """
                UPDATE shoporder 
                SET status = 'Dispatched' 
                WHERE shoporder.shoporderid = %s
            """
            cur.execute(query, (inputOrderId,))
            
            if cur.rowcount == 0:
                print(f"Update Failed: Order ID {inputOrderId} does not exist.")
                connection.rollback()
            else:
                connection.commit()
                print(f"Order {inputOrderId} successfully marked as Dispatched.")
                setPageView("vieworders")

        except Exception as dbError:
            connection.rollback()
            print(f"Database Error during dispatch: {dbError}")

    submitButton = ttk.Button(dispatchWindow, text="Confirm Dispatch", command=executeDispatchUpdate)
    submitButton.pack(pady=25)

def categoryDiscountReportTL(frame):
    discountReportWindow = tk.Toplevel(frame)
    discountReportWindow.title("Category Discount Preview")
    discountReportWindow.geometry("900x600")
    discountReportWindow.grab_set()

    tk.Label(discountReportWindow, text="Category Discount Preview Report", font=("Arial", 16)).pack(pady=10)

    inputFrame = tk.Frame(discountReportWindow)
    inputFrame.pack(pady=10)
    
    tk.Label(inputFrame, text="Category ID:").pack(side="left", padx=5)
    categoryIdEntry = ttk.Entry(inputFrame, width=10)
    categoryIdEntry.pack(side="left", padx=5)

    tk.Label(inputFrame, text="Discount %:").pack(side="left", padx=5)
    discountPercentEntry = ttk.Entry(inputFrame, width=10)
    discountPercentEntry.pack(side="left", padx=5)

    columnIdentifiers = ("bookId", "title", "publisherId", "standardPrice", "discountedPrice")
    reportTree = ttk.Treeview(discountReportWindow, columns=columnIdentifiers, show="headings")
    
    reportTree.heading("bookId", text="Book ID")
    reportTree.heading("title", text="Title")
    reportTree.heading("publisherId", text="Publisher ID")
    reportTree.heading("standardPrice", text="Standard Price")
    reportTree.heading("discountedPrice", text="Discounted Price")

    reportTree.column("bookId", width=100, anchor="center")
    reportTree.column("title", width=250, anchor="w")
    reportTree.column("publisherId", width=120, anchor="center")
    reportTree.column("standardPrice", width=120, anchor="e")
    reportTree.column("discountedPrice", width=120, anchor="e")

    reportTree.pack(fill="both", expand=True, padx=20, pady=5)

    def calculateDiscount():
        inputCategory = categoryIdEntry.get()
        inputDiscount = discountPercentEntry.get()

        if not inputCategory or not inputDiscount:
            return

        for row in reportTree.get_children():
            reportTree.delete(row)

        try:
            query = """
                SELECT 
                    book.bookid, 
                    book.title, 
                    book.publisherid, 
                    book.price, 
                    (book.price * (1 - (%s / 100.0)))
                FROM book
                WHERE book.categoryid = %s
            """ 
            cur.execute(query, (float(inputDiscount), inputCategory))
            results = cur.fetchall()

            for record in results:
                formattedOldPrice = f"£{record[3]:,.2f}"
                formattedNewPrice = f"£{record[4]:,.2f}"
                
                reportTree.insert("", "end", values=(
                    record[0], 
                    record[1], 
                    record[2], 
                    formattedOldPrice, 
                    formattedNewPrice
                ))

        except Exception as error:
            connection.rollback()
            print(f"Error calculating discounts: {error}")

    calculateButton = ttk.Button(inputFrame, text="Preview Discount", command=calculateDiscount)
    calculateButton.pack(side="left", padx=10)

    closeButton = tk.Button(discountReportWindow, text="Close", command=discountReportWindow.destroy)
    closeButton.pack(pady=10)

def generateSalesReportTL(frame):
    reportWindow = tk.Toplevel(frame)
    reportWindow.title("Sales Representative Performance Report")
    reportWindow.geometry("800x550")
    reportWindow.grab_set()

    tk.Label(reportWindow, text="Sales Representative Performance Report", font=("Arial", 16, "bold")).pack(pady=10)

    searchCriteriaFrame = tk.Frame(reportWindow)
    searchCriteriaFrame.pack(pady=10)
    
    tk.Label(searchCriteriaFrame, text="Start Date (YYYY-MM-DD):").pack(side="left", padx=5)
    startDateEntry = ttk.Entry(searchCriteriaFrame, width=12)
    startDateEntry.pack(side="left", padx=5)

    tk.Label(searchCriteriaFrame, text="End Date (YYYY-MM-DD):").pack(side="left", padx=5)
    endDateEntry = ttk.Entry(searchCriteriaFrame, width=12)
    endDateEntry.pack(side="left", padx=5)

    columnIdentifiers = ("repName", "totalUnits", "totalValue")
    salesReportTree = ttk.Treeview(reportWindow, columns=columnIdentifiers, show="headings")
    
    salesReportTree.heading("repName", text="Representative Name")
    salesReportTree.heading("totalUnits", text="Total Units Sold")
    salesReportTree.heading("totalValue", text="Total Order Value")

    salesReportTree.column("repName", width=250, anchor="w")
    salesReportTree.column("totalUnits", width=150, anchor="center")
    salesReportTree.column("totalValue", width=150, anchor="e")

    salesReportTree.pack(fill="both", expand=True, padx=20, pady=5)

    def executeReportGeneration():
        inputStartDate = startDateEntry.get()
        inputEndDate = endDateEntry.get()
        
        if not inputStartDate or not inputEndDate:
            return

        # Clear existing entries in the treeview before loading new data
        for existingRow in salesReportTree.get_children():
            salesReportTree.delete(existingRow)

        try:
            # L join ensures guys with no sales in the slot are still displayed
            query = """
                SELECT 
                    salesrep.name,
                    COALESCE(SUM(orderline.quantity), 0) AS totalUnitsSold,
                    COALESCE(SUM(orderline.quantity * orderline.unitsellingprice), 0) AS totalOrderValue
                FROM 
                    salesrep
                LEFT JOIN 
                    shoporder ON salesrep.salesrepid = shoporder.salesrepid 
                                 AND shoporder.orderdate >= %s 
                                 AND shoporder.orderdate <= %s
                LEFT JOIN 
                    orderline ON shoporder.shoporderid = orderline.shoporderid
                GROUP BY 
                    salesrep.salesrepid, salesrep.name
                ORDER BY 
                    totalOrderValue DESC
            """
            cur.execute(query, (inputStartDate, inputEndDate))
            reportResults = cur.fetchall()

            for currentRow in reportResults:
                formattedTotalOrderValue = f"£{currentRow[2]:,.2f}"
                
                salesReportTree.insert("", tk.END, values=(
                    currentRow[0], 
                    currentRow[1], 
                    formattedTotalOrderValue
                ))

        except Exception as databaseExecutionError:
            connection.rollback()
            print(f"Report Failure: {databaseExecutionError}")

    generateReportButton = ttk.Button(searchCriteriaFrame, text="Generate Report", command=executeReportGeneration)
    generateReportButton.pack(side="left", padx=15)

    closeReportButton = tk.Button(reportWindow, text="Close Report", command=reportWindow.destroy)
    closeReportButton.pack(pady=10)

def categoryReportTL(frame):
    reportWindow = tk.Toplevel(frame)
    reportWindow.title("Category Summary Report")
    reportWindow.geometry("600x500")

    tk.Label(reportWindow, text="Category Summary Report", font=("Arial", 15)).pack(pady=10)

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
        formattedPrice = f"£{row[2]:,.2f}" if row[2] is not None else "£0.00"
        reportTree.insert("", tk.END, values=(row[0], row[1], formattedPrice))

    cur.execute("SELECT COUNT(bookid), AVG(price) FROM book")
    summaryData = cur.fetchone()
    totalTitles = summaryData[0]
    overallAvg = f"£{summaryData[1]:,.2f}" if summaryData[1] is not None else "£0.00"


    summaryFrame = tk.Frame(reportWindow, relief="groove", bd=2)
    summaryFrame.pack(fill="x", padx=20, pady=15)

    tk.Label(summaryFrame, text="TOTALS:", font=("Arial", 10)).pack(side="left", padx=10)
    tk.Label(summaryFrame, text=f"Total Book Titles: {totalTitles}").pack(side="left", padx=20)
    tk.Label(summaryFrame, text=f"Overall Average Price: {overallAvg}").pack(side="right", padx=20)

    tk.Button(reportWindow, text="Close Report", command=reportWindow.destroy).pack(pady=10)

def addCategoryTL(frame):
    addCategoryWindow = tk.Toplevel(frame)
    addCategoryWindow.title("Create Category")
    addCategoryWindow.geometry("400x350")
    addCategoryWindow.grab_set()

    headerLabel = tk.Label(addCategoryWindow, text="Enter Category Information", font=("Arial", 16))
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

        setPageView("categories")

    submitButton = ttk.Button(addCategoryWindow, text="Submit Category", command=processCategorySubmission)
    submitButton.pack(pady=25)

def removeCategoryTL(frame):
    removeCategoryWindow = tk.Toplevel(frame)
    removeCategoryWindow.title("Remove Category")
    removeCategoryWindow.geometry("400x250")
    removeCategoryWindow.grab_set()

    headerLabel = tk.Label(removeCategoryWindow, text="Delete Category Record", font=("Arial", 16))
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
            query = "DELETE FROM Category WHERE CategoryID = %s"
            cur.execute(query, (targetCategoryId,))
            connection.commit()
        except:
            connection.rollback()
            return

        setPageView("categories")

    submitButton = ttk.Button(removeCategoryWindow, text="Remove Record", command=processCategoryRemoval)
    submitButton.pack(pady=25)

def addOrderLineTL(frame):
    addLineWindow = tk.Toplevel(frame)
    addLineWindow.title("Add Line to Order")
    addLineWindow.geometry("400x450")
    addLineWindow.grab_set()

    tk.Label(addLineWindow, text="New Order Line Entry").pack(pady=15)

    tk.Label(addLineWindow, text="Order ID:").pack()
    orderIdEntry = ttk.Entry(addLineWindow)
    orderIdEntry.pack(pady=5)

    tk.Label(addLineWindow, text="Book ID:").pack()
    bookIdEntry = ttk.Entry(addLineWindow)
    bookIdEntry.pack(pady=5)

    tk.Label(addLineWindow, text="Quantity to Add:").pack()
    quantityEntry = ttk.Entry(addLineWindow)
    quantityEntry.pack(pady=5)

    def processLineSubmission():
        targetOrder = orderIdEntry.get()
        targetBook = bookIdEntry.get()
        qtyToAdd = quantityEntry.get()

        if not targetOrder or not targetBook or not qtyToAdd:
            return

        try:
            query = "SELECT shoporder.status FROM shoporder WHERE shoporder.shoporderid = %s"
            cur.execute(query, (targetOrder,))
            orderStatusResult = cur.fetchone()

            if not orderStatusResult:
                print("Error: Order ID not found.")
                return
            
            currentStatus = orderStatusResult[0] if orderStatusResult[0] is not None else "Open"

            if currentStatus.lower() != "open":
                print(f"Transaction Blocked: Cannot add lines to a '{currentStatus}' order.")
                return

            # Check if this book is already in this order
            query = """
                SELECT orderline.quantity 
                FROM orderline 
                WHERE orderline.shoporderid = %s AND orderline.bookid = %s
            """
            cur.execute(query, (targetOrder, targetBook))
            existingLine = cur.fetchone()

            if existingLine:
                # If book exists, update the quantity
                query = """
                    UPDATE orderline 
                    SET quantity = orderline.quantity + %s 
                    WHERE orderline.shoporderid = %s AND orderline.bookid = %s
                """
                cur.execute(query, (qtyToAdd, targetOrder, targetBook))
                print(f"Updated quantity for Book {targetBook} in Order {targetOrder}.")
            else:
                # If book does not exist, insert a new line pull price from book table
                query = """
                    INSERT INTO orderline (shoporderid, quantity, bookid, unitsellingprice) 
                    SELECT %s, %s, book.bookid, book.price 
                    FROM book 
                    WHERE book.bookid = %s
                """
                cur.execute(query, (targetOrder, qtyToAdd, targetBook))
                print(f"Added new line for Book {targetBook} to Order {targetOrder}.")

            connection.commit()
            setPageView("vieworders")

        except Exception as error:
            connection.rollback()
            print(f"Database error: {error}")

    submitButton = ttk.Button(addLineWindow, text="Add Order Line", command=processLineSubmission)
    submitButton.pack(pady=25)

def bookOrderHistoryReportTL(frame):
    orderHistoryWindow = tk.Toplevel(frame)
    orderHistoryWindow.title("Book Order History")
    orderHistoryWindow.geometry("1000x650")
    orderHistoryWindow.grab_set()

    tk.Label(orderHistoryWindow, text="Book Order History Report", font=("Arial", 15)).pack(pady=10)

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
    
    totalCopiesOrderedLabel = tk.Label(summaryInformationFrame, text="Total Copies Ordered: 0", font=("Arial", 15))
    totalCopiesOrderedLabel.pack(side="left", padx=20)
    
    totalSellingValueLabel = tk.Label(summaryInformationFrame, text="Total Selling Value: £0.00", font=("Arial", 15))
    totalSellingValueLabel.pack(side="right", padx=20)

    def executeReportGeneration():
        targetBookIdentification = bookIdentificationEntry.get()
        if not targetBookIdentification:
            return

        for existingRow in orderHistoryTree.get_children():
            orderHistoryTree.delete(existingRow)

        try:

            query = """
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
            cur.execute(query, (targetBookIdentification,))
            historyResultRows = cur.fetchall()

            for currentRow in historyResultRows:
                orderHistoryTree.insert("", tk.END, values=(
                    currentRow[0], 
                    currentRow[1], 
                    f"£{currentRow[2]:,.2f}", 
                    f"£{currentRow[3]:,.2f}", 
                    currentRow[4], 
                    f"£{currentRow[5]:,.2f}", 
                    currentRow[6]
                ))

            query = """
                SELECT SUM(quantity), SUM(unitsellingprice * quantity) 
                FROM orderline 
                WHERE bookid = %s
            """
            cur.execute(query, (targetBookIdentification,))
            summaryDataResult = cur.fetchone()
            
            grandTotalCopies = summaryDataResult[0] if summaryDataResult[0] is not None else 0
            grandTotalSellingValue = summaryDataResult[1] if summaryDataResult[1] is not None else 0.0
            
            totalCopiesOrderedLabel.config(text=f"Total Copies Ordered: {grandTotalCopies}")
            totalSellingValueLabel.config(text=f"Total Selling Value: £{grandTotalSellingValue:,.2f}")

        except Exception as databaseExecutionError:
            connection.rollback()
            print(f"Report Failure: {databaseExecutionError}")

    generateReportButton = ttk.Button(searchCriteriaFrame, text="Generate History", command=executeReportGeneration)
    generateReportButton.pack(side="left", padx=10)

    closeReportButton = tk.Button(orderHistoryWindow, text="Close Report", command=orderHistoryWindow.destroy)
    closeReportButton.pack(pady=10)

# Defining helper functions

def getDBconnection():
    # Establishes connection to External Postgres Server
    # Returns Connection object - can be used to create cursor and cause rollback
    try:
        with open("pass.json") as connectionJson:
            connectionInfo = json.load(connectionJson)

        connection = psycopg2.connect(
            host=connectionInfo["host"],
            database=connectionInfo["database"],
            user=connectionInfo["user"],
            password=connectionInfo["password"],
            port=connectionInfo["port"]
        )
        return connection, connectionInfo["schema"]
    except Exception as e:
        print(f"connection failed, reason: {e}")
        return None, None

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
    "publishers" : shopAndPublishersPage,
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

connection, targetSchema = getDBconnection()
cur = connection.cursor()
cur.execute("SET search_path TO " + targetSchema)


setPageView("viewBooks")

# Event loop

root.mainloop()