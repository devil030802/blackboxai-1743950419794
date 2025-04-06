import sqlite3

def get_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect('dairy_management.db')
    return conn

def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        contact TEXT UNIQUE CHECK (LENGTH(contact) = 10)
    );
    ''')
    
    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        rate REAL NOT NULL CHECK (rate > 0)
    );
    ''')
    
    # Create DailyEntries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS DailyEntries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        entry_date DATE,
        product_id INTEGER,
        quantity REAL CHECK (quantity > 0),
        FOREIGN KEY (customer_id) REFERENCES Customers(id),
        FOREIGN KEY (product_id) REFERENCES Products(id)
    );
    ''')
    
    # Create Billing table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Billing (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        month TEXT CHECK (LENGTH(month) = 7), -- Format: YYYY-MM
        total REAL CHECK (total >= 0),
        paid REAL DEFAULT 0 CHECK (paid <= total),
        FOREIGN KEY (customer_id) REFERENCES Customers(id)
    );
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()