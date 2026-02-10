import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/orders.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Categories Table (To filter products professionally)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    ''')
    
    # 2. Products Table (With Category Relationship)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            category_id INTEGER,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            description TEXT,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
    ''')
    
    # 3. Orders Table (With Status and Timestamps)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            product_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Processing',
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    # --- SEEDING VAST DATA ---
    # Add Categories
    categories = [('Electronics',), ('Office Supplies',), ('Security Gear',)]
    cursor.executemany("INSERT OR IGNORE INTO categories (name) VALUES (?)", categories)
    
    # Add Vast Products
    products = [
        (1, 1, 'Precision Pro Laptop', 1450.00, 10, 'High-end workstation for AI devs.'),
        (2, 1, 'LiteBook Air', 950.00, 25, 'Portable and efficient for office work.'),
        (3, 1, 'SecureTab 10', 400.00, 40, 'Encrypted tablet for secure browsing.'),
        (4, 2, 'ErgoChair Executive', 350.00, 15, 'Ergonomic chair for long work hours.'),
        (5, 3, 'BioLock Door Handle', 220.00, 100, 'Biometric security for smart offices.'),
        (6, 3, 'Encrypted Flash Drive', 85.00, 200, '256-bit AES hardware encryption.'),
        (7, 1, 'UltraWide Monitor', 600.00, 12, '4K 34-inch curved productivity screen.')
    ]
    cursor.executemany("INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?, ?)", products)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("🚀 Vast Industrial Database Initialized!")