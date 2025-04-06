import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from ttkthemes import ThemedStyle
from database import get_connection, init_db
from customer import CustomerManager
from daily_entry import DailyEntryManager
from billing import BillingManager
from reports import ReportGenerator
from ui_utils import UIUtils

class DairyManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dairy Business Management System")
        self.root.geometry("1000x700")
        
        # Initialize database and create default products if needed
        init_db()
        self.create_default_products()
        
        # Apply modern theme
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content frame
        self.content_frame = ttk.Frame(self.main_container)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Initialize screens
        self.customer_manager = None
        self.daily_entry_manager = None
        self.billing_manager = None
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_sidebar(self):
        """Create navigation sidebar with buttons."""
        sidebar = ttk.Frame(self.main_container, width=200, relief=tk.RAISED)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Customers", self.show_customer_management),
            ("Daily Entry", self.show_daily_entry),
            ("Billing", self.show_billing),
            ("Reports", self.show_reports)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(sidebar, text=text, command=command)
            btn.pack(fill=tk.X, padx=5, pady=5)
    
    def create_default_products(self):
        """Create default products if they don't exist."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Products")
        if cursor.fetchone()[0] == 0:
            default_products = [
                ("Milk Type 1", 50.0),
                ("Milk Type 2", 55.0),
                ("Milk Type 3", 60.0),
                ("Paneer", 300.0),
                ("Chach", 40.0),
                ("Ghee", 500.0),
                ("Dahi", 60.0)
            ]
            cursor.executemany("INSERT INTO Products (name, rate) VALUES (?, ?)", default_products)
            conn.commit()
        conn.close()

    def show_dashboard(self):
        """Show dashboard screen with actual data."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Dashboard", font=('Helvetica', 16)).pack(pady=20)
        
        # Get data from database
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total customers
        cursor.execute("SELECT COUNT(*) FROM Customers")
        total_customers = cursor.fetchone()[0]
        
        # Today's entries
        cursor.execute("SELECT COUNT(*) FROM DailyEntries WHERE date(entry_date) = date('now')")
        today_entries = cursor.fetchone()[0]
        
        # Outstanding payments
        cursor.execute("SELECT SUM(total - paid) FROM Billing WHERE paid < total")
        outstanding = cursor.fetchone()[0] or 0
        
        conn.close()

        # Create dashboard widgets
        dashboard_frame = ttk.Frame(self.content_frame)
        dashboard_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ttk.Label(dashboard_frame, 
                text=f"Total Customers: {total_customers}", 
                font=('Helvetica', 12)).pack(anchor=tk.W, pady=5)
                
        ttk.Label(dashboard_frame, 
                text=f"Today's Entries: {today_entries}", 
                font=('Helvetica', 12)).pack(anchor=tk.W, pady=5)
                
        ttk.Label(dashboard_frame, 
                text=f"Outstanding Payments: ₹{outstanding:.2f}", 
                font=('Helvetica', 12)).pack(anchor=tk.W, pady=5)
    
    def show_customer_management(self):
        """Show customer management screen."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Customer Management", font=('Helvetica', 16)).pack(pady=20)
        
        # Add customer management widgets here
    
    def show_daily_entry(self):
        """Show daily entry screen."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Daily Entry", font=('Helvetica', 16)).pack(pady=20)
        
        # Add daily entry widgets here
    
    def show_billing(self):
        """Show billing screen."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Billing", font=('Helvetica', 16)).pack(pady=20)
        
        # Add billing widgets here
    
    def show_reports(self):
        """Show reports screen."""
        self.clear_content()
        ttk.Label(self.content_frame, text="Reports", font=('Helvetica', 16)).pack(pady=20)
        
        # Add report widgets here
    
    def clear_content(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DairyManagementApp(root)
    root.mainloop()