# create_database.py - UPDATED VERSION
import sqlite3
import os

def create_database():
    print("🚀 Starting SQL Database Creation...")
    
    # Create data directory if it doesn't exist
    os.makedirs('../data', exist_ok=True)
    
    # Create a connection to our database
    conn = sqlite3.connect('../data/ecommerce.db')
    cursor = conn.cursor()

    print("✅ Database connection created!")

    # Drop tables if they exist (for clean setup)
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS products')

    # Create Users Table
    cursor.execute('''
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        email TEXT NOT NULL,
        signup_date DATE,
        country TEXT
    )
    ''')

    # Create Products Table
    cursor.execute('''
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        price REAL
    )
    ''')

    # Create Orders Table
    cursor.execute('''
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_id INTEGER,
        order_date DATE,
        quantity INTEGER,
        amount REAL,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')

    print("✅ Tables created successfully!")

    # Add sample users
    users_data = [
        (1, 'alice@email.com', '2024-01-15', 'USA'),
        (2, 'bob@email.com', '2024-01-20', 'UK'),
        (3, 'carol@email.com', '2024-02-01', 'USA'),
        (4, 'david@email.com', '2024-02-10', 'Canada'),
        (5, 'eve@email.com', '2024-02-15', 'USA')
    ]

    cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', users_data)
    print("✅ Users data inserted!")

    # Add sample products
    products_data = [
        (101, 'Laptop', 'Electronics', 999.99),
        (102, 'Desk Chair', 'Furniture', 199.99),
        (103, 'Coffee Mug', 'Home', 12.99),
        (104, 'Wireless Mouse', 'Electronics', 29.99),
        (105, 'Notebook', 'Office', 8.99)
    ]

    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?)', products_data)
    print("✅ Products data inserted!")

    # Add sample orders
    orders_data = [
        (1001, 1, 101, '2024-02-01', 1, 999.99, 'delivered'),
        (1002, 1, 103, '2024-02-05', 2, 25.98, 'delivered'),
        (1003, 2, 102, '2024-02-10', 1, 199.99, 'shipped'),
        (1004, 3, 104, '2024-02-12', 1, 29.99, 'delivered'),
        (1005, 4, 105, '2024-02-14', 3, 26.97, 'processing'),
        (1006, 1, 104, '2024-02-15', 1, 29.99, 'shipped'),
        (1007, 5, 101, '2024-02-16', 1, 999.99, 'processing')
    ]

    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)', orders_data)
    print("✅ Orders data inserted!")

    conn.commit()
    print("✅ All data committed successfully!")

    # Verify data
    print("\n📊 Database Summary:")
    
    # Count records
    tables = ['users', 'products', 'orders']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {table.capitalize()}: {count} records")
    
    # Total revenue
    cursor.execute("SELECT SUM(amount) FROM orders")
    revenue = cursor.fetchone()[0]
    print(f"   Total Revenue: ${revenue:,.2f}")
    
    # Top customer
    cursor.execute('''
    SELECT u.email, SUM(o.amount) as total_spent 
    FROM users u JOIN orders o ON u.user_id = o.user_id 
    GROUP BY u.user_id 
    ORDER BY total_spent DESC 
    LIMIT 1
    ''')
    top_customer = cursor.fetchone()
    print(f"   Top Customer: {top_customer[0]} (${top_customer[1]:,.2f})")

    # Show sample data
    print("\n👥 Sample Users:")
    cursor.execute("SELECT * FROM users LIMIT 3")
    for row in cursor.fetchall():
        print(f"   User {row[0]}: {row[1]} from {row[3]}")

    conn.close()
    print("\n🎉 Database setup complete! Ready for SQL analysis.")

if __name__ == "__main__":
    create_database()
