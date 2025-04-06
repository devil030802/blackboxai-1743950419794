import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class DailyEntryManager:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_ui()
        self.load_products()

    def setup_ui(self):
        """Setup the daily entry UI components."""
        # Daily entry form frame
        form_frame = ttk.LabelFrame(self.parent, text="Daily Entry Form", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        # Form fields
        ttk.Label(form_frame, text="Date:").grid(row=0, column=0, sticky=tk.W)
        self.date_entry = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Customer:").grid(row=1, column=0, sticky=tk.W)
        self.customer_combobox = ttk.Combobox(form_frame)
        self.customer_combobox.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Product:").grid(row=2, column=0, sticky=tk.W)
        self.product_combobox = ttk.Combobox(form_frame)
        self.product_combobox.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W)
        self.quantity_entry = ttk.Entry(form_frame)
        self.quantity_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Add Entry", command=self.add_entry).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=2)

        # Daily entries list
        list_frame = ttk.LabelFrame(self.parent, text="Daily Entries", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=("date", "customer", "product", "quantity"), show="headings")
        self.tree.heading("date", text="Date")
        self.tree.heading("customer", text="Customer")
        self.tree.heading("product", text="Product")
        self.tree.heading("quantity", text="Quantity")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_products(self):
        """Load products from the database into the product combobox."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Products")
        products = cursor.fetchall()
        conn.close()

        self.product_combobox['values'] = [product[0] for product in products]

    def load_customers(self):
        """Load customers from the database into the customer combobox."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Customers")
        customers = cursor.fetchall()
        conn.close()

        self.customer_combobox['values'] = [customer[0] for customer in customers]

    def add_entry(self):
        """Add a new daily entry to the database."""
        date = self.date_entry.get()
        customer = self.customer_combobox.get()
        product = self.product_combobox.get()
        quantity = self.quantity_entry.get()

        if not customer or not product or not quantity:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO DailyEntries (entry_date, customer_id, product_id, quantity) VALUES (?, ?, ?, ?)",
                (date, self.get_customer_id(customer), self.get_product_id(product), quantity)
            )
            conn.commit()
            conn.close()
            self.load_entries()
            self.clear_form()
            messagebox.showinfo("Success", "Daily entry added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {str(e)}")

    def get_customer_id(self, customer_name):
        """Get customer ID from the database based on the name."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Customers WHERE name=?", (customer_name,))
        customer_id = cursor.fetchone()[0]
        conn.close()
        return customer_id

    def get_product_id(self, product_name):
        """Get product ID from the database based on the name."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Products WHERE name=?", (product_name,))
        product_id = cursor.fetchone()[0]
        conn.close()
        return product_id

    def load_entries(self):
        """Load daily entries from the database into the treeview."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT entry_date, (SELECT name FROM Customers WHERE id = customer_id) AS customer,
                   (SELECT name FROM Products WHERE id = product_id) AS product, quantity
            FROM DailyEntries
        ''')
        rows = cursor.fetchall()
        conn.close()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new items
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def clear_form(self):
        """Clear all form fields."""
        self.date_entry.set_date('')
        self.customer_combobox.set('')
        self.product_combobox.set('')
        self.quantity_entry.delete(0, tk.END)

    def on_customer_select(self, event):
        """Populate form fields when a customer is selected from the combobox."""
        selected = self.customer_combobox.get()
        if selected:
            self.load_products()