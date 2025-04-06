import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection

class CustomerManager:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_ui()
        self.load_customers()

    def setup_ui(self):
        """Setup the customer management UI components."""
        # Customer form frame
        form_frame = ttk.LabelFrame(self.parent, text="Customer Form", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        # Form fields
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Address:").grid(row=1, column=0, sticky=tk.W)
        self.address_entry = ttk.Entry(form_frame)
        self.address_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)

        ttk.Label(form_frame, text="Contact:").grid(row=2, column=0, sticky=tk.W)
        self.contact_entry = ttk.Entry(form_frame)
        self.contact_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Add", command=self.add_customer).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Update", command=self.update_customer).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_customer).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_form).pack(side=tk.LEFT, padx=2)

        # Customer list
        list_frame = ttk.LabelFrame(self.parent, text="Customer List", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=("id", "name", "address", "contact"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("address", text="Address")
        self.tree.heading("contact", text="Contact")
        self.tree.column("id", width=50)
        self.tree.column("name", width=150)
        self.tree.column("address", width=200)
        self.tree.column("contact", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Bind treeview selection
        self.tree.bind("<<TreeviewSelect>>", self.on_customer_select)

    def load_customers(self):
        """Load customers from database into treeview."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, address, contact FROM Customers")
        rows = cursor.fetchall()
        conn.close()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new items
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def add_customer(self):
        """Add a new customer to the database."""
        name = self.name_entry.get()
        address = self.address_entry.get()
        contact = self.contact_entry.get()

        if not name or not contact:
            messagebox.showerror("Error", "Name and Contact are required fields")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Customers (name, address, contact) VALUES (?, ?, ?)",
                (name, address, contact)
            )
            conn.commit()
            conn.close()
            self.load_customers()
            self.clear_form()
            messagebox.showinfo("Success", "Customer added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add customer: {str(e)}")

    def update_customer(self):
        """Update selected customer in the database."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No customer selected")
            return

        customer_id = self.tree.item(selected[0], "values")[0]
        name = self.name_entry.get()
        address = self.address_entry.get()
        contact = self.contact_entry.get()

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Customers SET name=?, address=?, contact=? WHERE id=?",
                (name, address, contact, customer_id)
            )
            conn.commit()
            conn.close()
            self.load_customers()
            messagebox.showinfo("Success", "Customer updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update customer: {str(e)}")

    def delete_customer(self):
        """Delete selected customer from the database."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No customer selected")
            return

        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            return

        customer_id = self.tree.item(selected[0], "values")[0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Customers WHERE id=?", (customer_id,))
            conn.commit()
            conn.close()
            self.load_customers()
            self.clear_form()
            messagebox.showinfo("Success", "Customer deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")

    def clear_form(self):
        """Clear all form fields."""
        self.name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)

    def on_customer_select(self, event):
        """Populate form fields when a customer is selected from the treeview."""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_form()
            self.name_entry.insert(0, values[1])
            self.address_entry.insert(0, values[2] if values[2] else "")
            self.contact_entry.insert(0, values[3])