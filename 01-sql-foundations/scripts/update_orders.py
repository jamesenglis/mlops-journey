# update_orders.py - Fix the dates for ML training
import sqlite3
from datetime import datetime, timedelta
import random

print("🔄 Updating order dates for realistic ML training...")

conn = sqlite3.connect('../data/ecommerce.db')
cursor = conn.cursor()

# Get current date for reference
today = datetime.now()

# Create more realistic order dates spread over time
new_orders = [
    # Recent orders (not churned)
    (1001, 1, 101, (today - timedelta(days=10)).strftime('%Y-%m-%d'), 1, 999.99, 'delivered'),
    (1006, 1, 104, (today - timedelta(days=5)).strftime('%Y-%m-%d'), 1, 29.99, 'shipped'),
    (1007, 5, 101, (today - timedelta(days=15)).strftime('%Y-%m-%d'), 1, 999.99, 'processing'),
    
    # Older orders (churned)
    (1002, 1, 103, (today - timedelta(days=120)).strftime('%Y-%m-%d'), 2, 25.98, 'delivered'),
    (1003, 2, 102, (today - timedelta(days=95)).strftime('%Y-%m-%d'), 1, 199.99, 'shipped'),
    (1004, 3, 104, (today - timedelta(days=110)).strftime('%Y-%m-%d'), 1, 29.99, 'delivered'),
    (1005, 4, 105, (today - timedelta(days=100)).strftime('%Y-%m-%d'), 3, 26.97, 'processing')
]

# Clear existing orders
cursor.execute('DELETE FROM orders')

# Insert updated orders
cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)', new_orders)
conn.commit()

print("✅ Updated order dates successfully!")

# Verify the mix
cursor.execute("""
SELECT 
    u.user_id,
    u.email,
    MAX(o.order_date) as last_order,
    CASE WHEN JULIANDAY('now') - JULIANDAY(MAX(o.order_date)) > 90 THEN 1 ELSE 0 END as is_churned
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id
""")

results = cursor.fetchall()
print("\n📊 Updated Customer Status:")
for user_id, email, last_order, is_churned in results:
    status = "🚨 CHURNED" if is_churned else "✅ ACTIVE"
    print(f"   {email}: {last_order} - {status}")

conn.close()
print("\n🎉 Database ready for ML training with realistic churn data!")