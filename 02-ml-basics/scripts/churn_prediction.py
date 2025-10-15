# churn_prediction.py - IMPROVED VERSION
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import numpy as np
import os

print("🎯 Starting Customer Churn Prediction Model...")

# FIXED: Better path handling
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '../../01-sql-foundations/data/ecommerce.db')

print(f"📁 Looking for database at: {db_path}")

# Check if database exists
if not os.path.exists(db_path):
    print(f"❌ Database not found at: {db_path}")
    print("🔍 Searching for database files...")
    
    # Search for any .db files
    for root, dirs, files in os.walk('../../'):
        for file in files:
            if file.endswith('.db'):
                print(f"   Found: {os.path.join(root, file)}")
    
    print("💡 Please make sure you've run the SQL database creation script first!")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Failed to connect to database: {e}")
    exit(1)

print("📊 Loading and preparing data...")

# Create a sophisticated query for feature engineering
query = """
SELECT 
    u.user_id,
    u.country,
    
    -- Behavioral Features
    COUNT(o.order_id) as total_orders,
    SUM(o.amount) as total_spent,
    AVG(o.amount) as avg_order_value,
    JULIANDAY('now') - JULIANDAY(MAX(o.order_date)) as days_since_last_order,
    COUNT(DISTINCT strftime('%Y-%m', o.order_date)) as active_months,
    
    -- Product Diversity
    COUNT(DISTINCT o.product_id) as unique_products_bought,
    
    -- Recent Activity (last 30 days)
    SUM(CASE WHEN o.order_date >= date('now', '-30 days') THEN 1 ELSE 0 END) as orders_last_30_days,
    SUM(CASE WHEN o.order_date >= date('now', '-30 days') THEN o.amount ELSE 0 END) as spent_last_30_days,
    
    -- Churn Label (90 days without order)
    CASE WHEN JULIANDAY('now') - JULIANDAY(MAX(o.order_date)) > 90 THEN 1 ELSE 0 END as is_churned
    
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
GROUP BY u.user_id, u.country
"""

# Load data into pandas
df = pd.read_sql_query(query, conn)
conn.close()

print(f"✅ Loaded {len(df)} customers with {df['is_churned'].sum()} churned customers")

# Handle customers with no orders
df.fillna(0, inplace=True)

# Prepare features and target
X = df.drop(['user_id', 'is_churned'], axis=1)
y = df['is_churned']

# Convert country to numerical (one-hot encoding)
X = pd.get_dummies(X, columns=['country'], prefix='country')

print(f"📈 Using {X.shape[1]} features for prediction")

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print(f"📚 Training set: {X_train.shape[0]} samples")
print(f"🧪 Test set: {X_test.shape[0]} samples")

# Train Random Forest model
print("🌲 Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'  # Handle imbalanced data
)

model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"\n📊 MODEL PERFORMANCE:")
print(f"   Accuracy: {accuracy:.3f}")
print(f"   Churn Detection Rate: {y_pred.sum()}/{y_test.sum()}")

print("\n" + "="*50)
print("📋 Detailed Classification Report:")
print("="*50)
print(classification_report(y_test, y_pred, target_names=['Not Churned', 'Churned']))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🔍 TOP 10 MOST IMPORTANT FEATURES:")
print(feature_importance.head(10))

# Save the model (create models directory if needed)
models_dir = os.path.join(script_dir, '../models')
os.makedirs(models_dir, exist_ok=True)

model_path = os.path.join(models_dir, 'churn_predictor.pkl')
joblib.dump(model, model_path)
print(f"\n💾 Model saved to: {model_path}")

# Save feature names for later use
feature_names_path = os.path.join(models_dir, 'feature_names.pkl')
joblib.dump(list(X.columns), feature_names_path)

# Create a sample prediction
sample_customer = X_test.iloc[0:1]
prediction = model.predict(sample_customer)[0]
probability = model.predict_proba(sample_customer)[0][1]

print(f"\n🎯 SAMPLE PREDICTION:")
print(f"   Actual: {'Churned' if y_test.iloc[0] else 'Not Churned'}")
print(f"   Predicted: {'Churned' if prediction else 'Not Churned'}")
print(f"   Churn Probability: {probability:.3f}")

print("\n🎉 Churn prediction model training complete!")
print("   Next: Use the model to predict on new customers!")