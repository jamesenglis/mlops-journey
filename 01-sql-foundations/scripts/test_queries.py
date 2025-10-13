# test_queries.py - CORRECTED VERSION
import sqlite3
import os

def test_queries():
    # Correct path to the database
    db_path = '../data/ecommerce.db'
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        print("Please run create_database.py first!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🧪 Testing SQL Queries...")
    
    # Query 1: Total sales by country
    print("\n1. 📊 Total Sales by Country:")
    cursor.execute('''
    SELECT 
        u.country,
        COUNT(o.order_id) as total_orders,
        SUM(o.amount) as total_revenue
    FROM users u
    JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.country
    ORDER BY total_revenue DESC
    ''')
    
    for row in cursor.fetchall():
        print(f"   {row[0]}: {row[1]} orders, ${row[2]:,.2f} revenue")
    
    # Query 2: Best selling products
    print("\n2. 🏆 Best Selling Products:")
    cursor.execute('''
    SELECT 
        p.product_name,
        p.category,
        SUM(o.quantity) as total_sold,
        SUM(o.amount) as total_revenue
    FROM products p
    JOIN orders o ON p.product_id = o.product_id
    GROUP BY p.product_id
    ORDER BY total_revenue DESC
    LIMIT 3
    ''')
    
    for row in cursor.fetchall():
        print(f"   {row[0]} ({row[1]}): {row[2]} sold, ${row[3]:,.2f}")
    
    # Query 3: Customer orders summary
    print("\n3. 👥 Customer Order Summary:")
    cursor.execute('''
    SELECT 
        u.email,
        u.country,
        COUNT(o.order_id) as order_count,
        SUM(o.amount) as total_spent
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    GROUP BY u.user_id
    ORDER BY total_spent DESC
    ''')
    
    for row in cursor.fetchall():
        orders = row[2] if row[2] else 0
        spent = row[3] if row[3] else 0
        print(f"   {row[0]} ({row[1]}): {orders} orders, ${spent:.2f} spent")
    
    conn.close()
    print("\n✅ All queries executed successfully!")

if __name__ == "__main__":
    test_queries()