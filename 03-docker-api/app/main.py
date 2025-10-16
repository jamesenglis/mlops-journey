# FastAPI ML Application
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import sqlite3
import os
from typing import List, Optional

app = FastAPI(
    title="Customer Churn Prediction API",
    description="ML API for predicting customer churn from e-commerce data",
    version="1.0.0"
)

# Load model once at startup
model = None
feature_names = None

@app.on_event("startup")
async def load_model():
    global model, feature_names
    try:
        model_path = "../models/churn_predictor.pkl"
        feature_path = "../models/feature_names.pkl"
        
        model = joblib.load(model_path)
        feature_names = joblib.load(feature_path)
        
        print("✅ ML Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")

class CustomerData(BaseModel):
    user_id: int

class PredictionResponse(BaseModel):
    user_id: int
    churn_probability: float
    will_churn: bool
    risk_level: str
    recommendation: str
    status: str

@app.get("/")
async def root():
    return {
        "message": "🚀 Customer Churn Prediction API is running!",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict/{user_id}",
            "batch_predict": "/predict/batch"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "message": "API is ready for predictions!"
    }

@app.get("/predict/{user_id}", response_model=PredictionResponse)
async def predict_churn(user_id: int):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Get customer data from SQL database
        db_path = "../../01-sql-foundations/data/ecommerce.db"
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
            raise HTTPException(status_code=404, detail=f"Customer {user_id} not found")
        
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
        recommendation = "Offer retention discount" if will_churn else "Continue normal engagement"
        
        return PredictionResponse(
            user_id=user_id,
            churn_probability=round(churn_probability, 3),
            will_churn=will_churn,
            risk_level=risk_level,
            recommendation=recommendation,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch")
async def batch_predict(customer_ids: List[int]):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for user_id in customer_ids:
        try:
            # Reuse the prediction logic from single prediction
            prediction = await predict_churn(user_id)
            results.append(prediction.dict())
        except Exception as e:
            results.append({
                "user_id": user_id,
                "error": str(e),
                "status": "failed"
            })
    
    return {
        "predictions": results,
        "total_processed": len(results)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)