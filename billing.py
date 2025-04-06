import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class BillingManager:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_ui()

    def setup_ui(self):
        """Setup the billing UI components."""
        # Billing form frame
        form_frame = ttk.LabelFrame(self.parent, text="Billing Calculator", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        # Month selection
        ttk.Label(form_frame, text="Select Month:").grid(row=0, column=0, sticky=tk.W)
        self.month_entry = ttk.Entry(form_frame)
        self.month_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Calculate Billing", command=self.calculate_billing).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Export to Excel", command=self.export_to_excel).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Export to PDF", command=self.export_to_pdf).pack(side=tk.LEFT, padx=2)

        # Billing summary list
        list_frame = ttk.LabelFrame(self.parent, text="Billing Summary", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(list_frame, columns=("customer", "total", "paid"), show="headings")
        self.tree.heading("customer", text="Customer")
        self.tree.heading("total", text="Total")
        self.tree.heading("paid", text="Paid")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def calculate_billing(self):
        """Calculate billing for the selected month."""
        month = self.month_entry.get()
        if not month:
            messagebox.showerror("Error", "Please enter a month in YYYY-MM format")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT (SELECT name FROM Customers WHERE id = customer_id) AS customer,
                   SUM(quantity * (SELECT rate FROM Products WHERE id = product_id)) AS total
            FROM DailyEntries
            WHERE strftime('%Y-%m', entry_date) = ?
            GROUP BY customer_id
        ''', (month,))
        rows = cursor.fetchall()
        conn.close()

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new items
        for row in rows:
            self.tree.insert("", tk.END, values=row)

        messagebox.showinfo("Success", "Billing calculated successfully")

    def export_to_excel(self):
        """Export billing summary to Excel."""
        month = self.month_entry.get()
        if not month:
            messagebox.showerror("Error", "Please enter a month in YYYY-MM format")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT (SELECT name FROM Customers WHERE id = customer_id) AS customer,
                   SUM(quantity * (SELECT rate FROM Products WHERE id = product_id)) AS total
            FROM DailyEntries
            WHERE strftime('%Y-%m', entry_date) = ?
            GROUP BY customer_id
        ''', (month,))
        rows = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(rows, columns=["Customer", "Total"])
        df.to_excel(f'billing_summary_{month}.xlsx', index=False)
        messagebox.showinfo("Success", f"Billing summary exported to billing_summary_{month}.xlsx")

    def export_to_pdf(self):
        """Export billing summary to PDF."""
        month = self.month_entry.get()
        if not month:
            messagebox.showerror("Error", "Please enter a month in YYYY-MM format")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT (SELECT name FROM Customers WHERE id = customer_id) AS customer,
                   SUM(quantity * (SELECT rate FROM Products WHERE id = product_id)) AS total
            FROM DailyEntries
            WHERE strftime('%Y-%m', entry_date) = ?
            GROUP BY customer_id
        ''', (month,))
        rows = cursor.fetchall()
        conn.close()

        pdf_file = f'billing_summary_{month}.pdf'
        c = canvas.Canvas(pdf_file, pagesize=letter)
        c.drawString(100, 750, f"Billing Summary for {month}")
        c.drawString(100, 730, "Customer")
        c.drawString(300, 730, "Total")

        y = 710
        for row in rows:
            c.drawString(100, y, row[0])
            c.drawString(300, y, str(row[1]))
            y -= 20

        c.save()
        messagebox.showinfo("Success", f"Billing summary exported to {pdf_file}")