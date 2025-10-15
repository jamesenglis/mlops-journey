# predict_churn.py
import sqlite3
import pandas as pd
import joblib
import numpy as np
import os

def predict_customer_churn(user_id):
    """Predict churn probability for a specific customer"""
    
    # Load the trained model
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, '../models/churn_predictor.pkl')
    feature_names_path = os.path.join(script_dir, '../models/feature_names.pkl')
    
    model = joblib.load(model_path)
    feature_names = joblib.load(feature_names_path)
    
    # Get customer data
    db_path = os.path.join(script_dir, '../../01-sql-foundations/data/ecommerce.db')
    conn = sqlite3.connect(db_path)
    
    query = f"""
    SELECT 
        u.user_id,
        u.country,
        COUNT(o.order_id) as total_orders,
        SUM(o.amount) as total_spent,
        AVG(o.amount) as avg_order_value,
        JULIANDAY('now') - JULIANDAY(MAX(o.order_date)) as days_since_last_order,
        COUNT(DISTINCT strftime('%Y-%m', o.order_date)) as active_months,
        COUNT(DISTINCT o.product_id) as unique_products_bought,
        SUM(CASE WHEN o.order_date >= date('now', '-30 days') THEN 1 ELSE 0 END) as orders_last_30_days,
        SUM(CASE WHEN o.order_date >= date('now', '-30 days') THEN o.amount ELSE 0 END) as spent_last_30_days
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id
    WHERE u.user_id = {user_id}
    GROUP BY u.user_id, u.country
    """
    
    customer_data = pd.read_sql_query(query, conn)
    conn.close()
    
    if customer_data.empty:
        return f"❌ Customer {user_id} not found!"
    
    # Prepare features
    features = customer_data.drop(['user_id'], axis=1)
    features = pd.get_dummies(features, columns=['country'], prefix='country')
    
    # Ensure all training features are present
    for feature in feature_names:
        if feature not in features.columns:
            features[feature] = 0
    
    features = features[feature_names]
    
    # Make prediction
    churn_probability = model.predict_proba(features)[0][1]
    will_churn = churn_probability > 0.5
    
    # Interpret results
    risk_level = "HIGH" if churn_probability > 0.7 else "MEDIUM" if churn_probability > 0.3 else "LOW"
    
    return {
        'user_id': user_id,
        'churn_probability': round(churn_probability, 3),
        'will_churn': will_churn,
        'risk_level': risk_level,
        'recommendation': "🚨 Offer retention discount" if will_churn else "✅ Continue normal engagement"
    }

# Test the function
if __name__ == "__main__":
    print("🔮 Customer Churn Predictor")
    print("=" * 50)
    
    # Test with all customers
    test_customers = [1, 2, 3, 4, 5]
    
    for customer_id in test_customers:
        result = predict_customer_churn(customer_id)
        if isinstance(result, dict):
            print(f"\n👤 Customer {result['user_id']}:")
            print(f"   📊 Churn Probability: {result['churn_probability']}")
            print(f"   🎯 Prediction: {'🚨 WILL CHURN' if result['will_churn'] else '✅ WILL STAY'}")
            print(f"   ⚠️  Risk Level: {result['risk_level']}")
            print(f"   💡 Recommendation: {result['recommendation']}")
        else:
            print(result)
    
    print("\n" + "=" * 50)
    print("🎉 All predictions completed!")