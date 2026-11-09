
class Product:  #class to represent a product in the store
    #this initializes the product with its code, name, price, and stock
    def __init__(self, code, name, price, stock):
        self.code = code
        self.name = name
        self.price = price
        self.stock = stock

#TO manage the store's products and sales, we create a Store class
class Store:
    def __init__(self):
        self.products = []
        self.sales = []
        self.deleted_codes = set()
        #Default products are added to the store when it is initialized
        self.add_product("P01", "Notebook", 8.00, 10)
        self.add_product("P02", "Pen", 2.00, 10)
        self.add_product("P03", "USB Drive", 25.00, 10)
        self.add_product("P04", "Water Bottle", 5.00, 10)
        self.add_product("P05", "Calculator", 35.00, 10)

    # find a product by its code and return it if found, otherwise return None
    def find_product(self, code):
        for product in self.products:
            if product.code.lower() == code.lower():
                return product
        return None

    # Add a new product, ensuring that the code is unique and not reused from deleted products
    def add_product(self, code, name, price, stock):
        code = code.strip()
        name = name.strip()
        # Validate inputs
        if code == "" or name == "":
            raise ValueError("Code and name cannot be blank.")
        # Check if the code has been deleted before
        if code.lower() in self.deleted_codes:
            raise ValueError("Deleted codes cannot be reused.")
        # Check if the product code already exists,and if so, raise an error
        if self.find_product(code) is not None:
            raise ValueError("Product code already exists.")
        # Validate price and stock
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        # Validate stock to ensure it is a non-negative whole number
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        # Create a new product and add it to the products list,and also add the code to the deleted_codes set to prevent reuse
        product = Product(code, name, price, stock)
        self.products.append(product)

    # Edit an existing product,and validate the inputs to ensure they are correct and do not violate any constraints
    def edit_product(self, code, name=None, price=None, stock=None):
        product = self.find_product(code)
        # If the product is not found, raise an error
        if product is None:
            raise ValueError("Product not found.")
        # Validate and update the product's name, price, and stock if provided
        if name is not None:
            if name.strip() == "":
                raise ValueError("Name cannot be blank.")
            product.name = name.strip()
        # Validate and update the product's price if provided, ensuring it is greater than zero
        if price is not None:
            if price <= 0:
                raise ValueError("Price must be greater than zero.")
            product.price = price
        # Validate and update the product's stock if provided, ensuring it is a non-negative whole number
        if stock is not None:
            if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
                raise ValueError("Stock must be a non-negative whole number.")
            product.stock = stock

    # Search products by name
    def search_products(self, search_text):
        search_text = search_text.strip().lower()

        if search_text == "":
            return self.products.copy()

        results = []

        for product in self.products:
            if search_text in product.name.lower():
                results.append(product)

        return results

    # Delete a product
    def delete_product(self, code):
        product = self.find_product(code)

        if product is None:
            raise ValueError("Product not found.")

        self.products.remove(product)
        self.deleted_codes.add(product.code.lower())

    # Display all products
    def view_products(self):
        return self.products

# .......................................................... Stept 2 >>>>>>>>>>>>>>>>>>>>>>

    # Record a new sale
    def sell_product(self, code, quantity):

        # Find the product
        product = self.find_product(code)

        if product is None:
            raise ValueError("Product not found.")

        # Validate quantity
        if not isinstance(quantity, int) or isinstance(quantity, bool):
            raise ValueError("Quantity must be a whole number.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        # Check available stock
        if quantity > product.stock:
            raise ValueError("Not enough stock available.")

        # Calculate subtotal
        subtotal = product.price * quantity

        # Calculate discount
        if quantity >= 5:
            discount = subtotal * 0.10
        else:
            discount = 0

        # Calculate final bill
        final_bill = subtotal - discount

        # Update stock
        product.stock -= quantity

        # Save sale information
        sale_number = len(self.sales) + 1

        sale = [
            sale_number,
            product.code,
            quantity,
            final_bill
        ]

        self.sales.append(sale)

        # Return receipt information
        receipt = {
            "product": product.name,
            "quantity": quantity,
            "subtotal": subtotal,
            "discount": discount,
            "final_bill": final_bill,
            "remaining_stock": product.stock
        }

        return receipt

    # Display sales history
    def sales_history(self):

        return self.sales

    # Generate sales report
    def sales_report(self):

        if len(self.sales) == 0:
            return {
                "message": "No sales recorded",
                "number_of_sales": 0,
                "total_units": 0,
                "total_revenue": 0.00
            }

        number_of_sales = len(self.sales)
        total_units = 0
        total_revenue = 0.00

        # Calculate report totals using a loop
        for sale in self.sales:
            total_units += sale[2]
            total_revenue += sale[3]

        report = {
            "message": "Sales Report",
            "number_of_sales": number_of_sales,
            "total_units": total_units,
            "total_revenue": total_revenue
        }

        return report

# كود الواجهة الرسومية (GUI) باستخدام Tkinter

import tkinter as tk
from tkinter import ttk, messagebox


# Create the main application window
root = tk.Tk()
root.title("My Campus Store Manager")
root.geometry("900x700")
root.resizable(True, True)

# Create Store object
store = Store()


# Display results and messages
def display_result(message):
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, message)
    result_text.config(state="disabled")


# Read and validate whole numbers
def get_integer(value, field_name):
    value = value.strip()

    if value == "":
        raise ValueError(field_name + " cannot be blank.")

    if not value.isdigit():
        raise ValueError(field_name + " must be a whole number.")

    return int(value)


# Read and validate price
def get_price(value):
    value = value.strip()

    if value == "":
        raise ValueError("Price cannot be blank.")

    try:
        price = float(value)
    except ValueError:
        raise ValueError("Price must be a valid number.")

    if price <= 0:
        raise ValueError("Price must be greater than zero.")

    return price


# Add a new product
def add_product():
    try:
        code = code_entry.get()
        name = name_entry.get()
        price = get_price(price_entry.get())
        stock = get_integer(stock_entry.get(), "Stock")

        store.add_product(code, name, price, stock)

        display_result("Product added successfully!")

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))


# Edit an existing product
def edit_product():
    try:
        code = code_entry.get().strip()

        if code == "":
            raise ValueError("Enter the product code.")

        name = name_entry.get().strip()
        price_value = price_entry.get().strip()
        stock_value = stock_entry.get().strip()

        # Empty fields mean no change
        price = None
        stock = None

        if price_value != "":
            price = get_price(price_value)

        if stock_value != "":
            stock = get_integer(stock_value, "Stock")

        if name == "":
            name = None

        store.edit_product(
            code,
            name=name,
            price=price,
            stock=stock
        )

        display_result("Product updated successfully!")

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))


# Search for products
def search_product():
    search_text = search_entry.get()

    results = store.search_products(search_text)

    if len(results) == 0:
        display_result("No products found.")
        return

    output = "SEARCH RESULTS\n"
    output += "-" * 65 + "\n"

    for product in results:
        output += (
            f"Code: {product.code} | "
            f"Name: {product.name} | "
            f"Price: SAR {product.price:.2f} | "
            f"Stock: {product.stock}\n"
        )

    display_result(output)


# Delete a product
def delete_product():
    try:
        code = code_entry.get().strip()

        if code == "":
            raise ValueError("Enter the product code.")

        product = store.find_product(code)

        if product is None:
            raise ValueError("Product not found.")

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete "
            + product.name + "?"
        )

        if confirm:
            store.delete_product(code)
            display_result("Product deleted successfully!")

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))


# Display all products
def view_products():
    products = store.view_products()

    output = "PRODUCT LIST\n"
    output += "=" * 70 + "\n"
    output += (
        f"{'Code':<12}"
        f"{'Name':<22}"
        f"{'Price (SAR)':<17}"
        f"{'Stock':<10}\n"
    )
    output += "-" * 70 + "\n"

    for product in products:
        output += (
            f"{product.code:<12}"
            f"{product.name:<22}"
            f"{product.price:<17.2f}"
            f"{product.stock:<10}\n"
        )

    display_result(output)


# Record a new sale
def record_sale():
    try:
        code = code_entry.get().strip()
        quantity = get_integer(
            quantity_entry.get(),
            "Sale quantity"
        )

        receipt = store.sell_product(code, quantity)

        output = "SALES RECEIPT\n"
        output += "=" * 40 + "\n"
        output += f"Product: {receipt['product']}\n"
        output += f"Quantity: {receipt['quantity']}\n"
        output += (
            f"Subtotal: SAR "
            f"{receipt['subtotal']:.2f}\n"
        )
        output += (
            f"Discount: SAR "
            f"{receipt['discount']:.2f}\n"
        )
        output += (
            f"Final Bill: SAR "
            f"{receipt['final_bill']:.2f}\n"
        )
        output += "-" * 40 + "\n"
        output += (
            f"Remaining Stock: "
            f"{receipt['remaining_stock']}\n"
        )
        output += "=" * 40

        display_result(output)

    except ValueError as error:
        messagebox.showerror("Sale Error", str(error))


# Display sales history
def show_sales_history():
    sales = store.sales_history()

    if len(sales) == 0:
        display_result("No sales recorded.")
        return

    output = "SALES HISTORY\n"
    output += "=" * 65 + "\n"

    for sale in sales:
        output += (
            f"Sale Number: {sale[0]} | "
            f"Product Code: {sale[1]} | "
            f"Quantity: {sale[2]} | "
            f"Final Bill: SAR {sale[3]:.2f}\n"
        )

    display_result(output)


# Display sales report
def show_sales_report():
    report = store.sales_report()

    output = "SALES REPORT\n"
    output += "=" * 40 + "\n"
    output += report["message"] + "\n"
    output += "-" * 40 + "\n"

    output += (
        f"Number of Sales: "
        f"{report['number_of_sales']}\n"
    )

    output += (
        f"Total Units Sold: "
        f"{report['total_units']}\n"
    )

    output += (
        f"Total Revenue: SAR "
        f"{report['total_revenue']:.2f}\n"
    )

    output += "=" * 40

    display_result(output)


# Main title
title_label = ttk.Label(
    root,
    text="My Campus Store Manager",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=15)


# Product information frame
product_frame = ttk.LabelFrame(
    root,
    text="Product Information",
    padding=10
)
product_frame.pack(fill="x", padx=20, pady=5)

# Product Code
ttk.Label(product_frame, text="Product Code:").grid(
    row=0, column=0, padx=5, pady=8, sticky="w"
)

code_entry = ttk.Entry(product_frame, width=25)
code_entry.grid(row=0, column=1, padx=5, pady=8)

# Product Name
ttk.Label(product_frame, text="Product Name:").grid(
    row=0, column=2, padx=5, pady=8, sticky="w"
)

name_entry = ttk.Entry(product_frame, width=25)
name_entry.grid(row=0, column=3, padx=5, pady=8)

# Product Price
ttk.Label(product_frame, text="Price (SAR):").grid(
    row=1, column=0, padx=5, pady=8, sticky="w"
)

price_entry = ttk.Entry(product_frame, width=25)
price_entry.grid(row=1, column=1, padx=5, pady=8)

# Product Stock
ttk.Label(product_frame, text="Stock:").grid(
    row=1, column=2, padx=5, pady=8, sticky="w"
)

stock_entry = ttk.Entry(product_frame, width=25)
stock_entry.grid(row=1, column=3, padx=5, pady=8)


# Search and sales frame
search_frame = ttk.LabelFrame(
    root,
    text="Search and Sales Information",
    padding=10
)
search_frame.pack(fill="x", padx=20, pady=5)

ttk.Label(search_frame, text="Search Text:").grid(
    row=0, column=0, padx=5, pady=8
)

search_entry = ttk.Entry(search_frame, width=25)
search_entry.grid(row=0, column=1, padx=5, pady=8)

ttk.Label(search_frame, text="Sale Quantity:").grid(
    row=0, column=2, padx=5, pady=8
)

quantity_entry = ttk.Entry(search_frame, width=25)
quantity_entry.grid(row=0, column=3, padx=5, pady=8)


# Product management buttons
management_frame = ttk.LabelFrame(
    root,
    text="Product Management",
    padding=10
)
management_frame.pack(fill="x", padx=20, pady=5)

ttk.Button(
    management_frame,
    text="Add",
    command=add_product
).grid(row=0, column=0, padx=8, pady=8)

ttk.Button(
    management_frame,
    text="Edit",
    command=edit_product
).grid(row=0, column=1, padx=8, pady=8)

ttk.Button(
    management_frame,
    text="Search",
    command=search_product
).grid(row=0, column=2, padx=8, pady=8)

ttk.Button(
    management_frame,
    text="Delete",
    command=delete_product
).grid(row=0, column=3, padx=8, pady=8)

ttk.Button(
    management_frame,
    text="View Products",
    command=view_products
).grid(row=0, column=4, padx=8, pady=8)


# Sales management buttons
sales_frame = ttk.LabelFrame(
    root,
    text="Sales Management",
    padding=10
)
sales_frame.pack(fill="x", padx=20, pady=5)

ttk.Button(
    sales_frame,
    text="Record Sale",
    command=record_sale
).grid(row=0, column=0, padx=20, pady=8)

ttk.Button(
    sales_frame,
    text="Sales History",
    command=show_sales_history
).grid(row=0, column=1, padx=20, pady=8)

ttk.Button(
    sales_frame,
    text="Sales Report",
    command=show_sales_report
).grid(row=0, column=2, padx=20, pady=8)


# Results and messages area
result_frame = ttk.LabelFrame(
    root,
    text="Results and Messages",
    padding=10
)
result_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)

result_text = tk.Text(
    result_frame,
    height=12,
    font=("Consolas", 10),
    wrap="none",
    state="disabled"
)

result_scrollbar = ttk.Scrollbar(
    result_frame,
    orient="vertical",
    command=result_text.yview
)

result_text.configure(
    yscrollcommand=result_scrollbar.set
)

result_scrollbar.pack(side="right", fill="y")
result_text.pack(fill="both", expand=True)


# Show initial product list
view_products()


# Run the application
root.mainloop()



