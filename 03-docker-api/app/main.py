from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Churn Prediction API", version="1.0.0")

# Global variables for model and features
model = None
feature_names = None

class CustomerData(BaseModel):
    age: int
    tenure: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    support_calls: int

def load_model():
    """Load the model and feature names with comprehensive debugging"""
    global model, feature_names
    
    logger.info("🔍 STARTING MODEL LOAD DEBUGGING")
    
    # Debug: Current directory and files
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info("Contents of current directory:")
    for item in os.listdir('.'):
        logger.info(f"  📁 {item}")
    
    # Debug: Check app directory
    app_dir = '/app' if os.path.exists('/app') else '.'
    logger.info(f"App directory: {app_dir}")
    logger.info(f"Contents of {app_dir}:")
    if os.path.exists(app_dir):
        for item in os.listdir(app_dir):
            item_path = os.path.join(app_dir, item)
            item_type = "📁 DIR" if os.path.isdir(item_path) else "📄 FILE"
            logger.info(f"  {item_type} {item}")
    
    # Debug: Check models directory
    models_path = '/app/models' if os.path.exists('/app/models') else './models'
    logger.info(f"Models path: {models_path}")
    
    if os.path.exists(models_path):
        logger.info(f"Contents of {models_path}:")
        for item in os.listdir(models_path):
            item_path = os.path.join(models_path, item)
            item_type = "📁 DIR" if os.path.isdir(item_path) else "📄 FILE"
            size = os.path.getsize(item_path) if os.path.isfile(item_path) else "N/A"
            logger.info(f"  {item_type} {item} ({size} bytes)")
    else:
        logger.error(f"❌ Models directory does not exist: {models_path}")
    
    # Try to load model
    model_path = os.path.join(models_path, 'churn_predictor.pkl')
    features_path = os.path.join(models_path, 'feature_names.pkl')
    
    logger.info(f"Model path: {model_path}")
    logger.info(f"Features path: {features_path}")
    
    try:
        if os.path.exists(model_path):
            logger.info(f"✅ Model file exists: {model_path}")
            model = joblib.load(model_path)
            logger.info("✅ Model loaded successfully!")
        else:
            logger.error(f"❌ Model file not found: {model_path}")
            
        if os.path.exists(features_path):
            logger.info(f"✅ Features file exists: {features_path}")
            feature_names = joblib.load(features_path)
            logger.info(f"✅ Features loaded: {feature_names}")
        else:
            logger.error(f"❌ Features file not found: {features_path}")
            
    except Exception as e:
        logger.error(f"❌ Error loading model/features: {e}")
        # Create fallback model for testing
        logger.info("🔄 Creating fallback model for testing...")
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import make_classification
        
        X, y = make_classification(n_samples=100, n_features=6, random_state=42)
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        feature_names = ['age', 'tenure', 'monthly_charges', 'total_charges', 
                        'support_calls', 'contract_type_Monthly', 'contract_type_Yearly', 'contract_type_Two-year']
        logger.info("✅ Fallback model created for testing")

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("🚀 Starting up Churn Prediction API...")
    load_model()

@app.get("/")
def read_root():
    return {
        "message": "Churn Prediction API is running!",
        "model_loaded": model is not None,
        "features_loaded": feature_names is not None
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "features_loaded": feature_names is not None
    }

@app.get("/debug")
def debug_info():
    """Endpoint to get debug information"""
    models_path = '/app/models' if os.path.exists('/app/models') else './models'
    model_path = os.path.join(models_path, 'churn_predictor.pkl')
    features_path = os.path.join(models_path, 'feature_names.pkl')
    
    return {
        "current_directory": os.getcwd(),
        "app_directory_exists": os.path.exists('/app'),
        "models_directory_exists": os.path.exists(models_path),
        "model_file_exists": os.path.exists(model_path),
        "features_file_exists": os.path.exists(features_path),
        "model_loaded": model is not None,
        "features_loaded": feature_names is not None,
        "container_files": {
            "root": os.listdir('/') if os.path.exists('/') else [],
            "app": os.listdir('/app') if os.path.exists('/app') else [],
            "models": os.listdir(models_path) if os.path.exists(models_path) else []
        }
    }

@app.post("/predict")
def predict_churn(customer: CustomerData):
    if model is None or feature_names is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    try:
        # Convert to DataFrame
        input_data = pd.DataFrame([customer.dict()])
        
        # One-hot encoding for contract_type
        input_processed = pd.get_dummies(input_data)
        
        # Ensure all expected columns are present
        for col in feature_names:
            if col not in input_processed.columns:
                input_processed[col] = 0
        
        # Reorder columns to match training
        input_processed = input_processed[feature_names]
        
        prediction = model.predict(input_processed)[0]
        probability = model.predict_proba(input_processed)[0][1]
        
        return {
            "churn_prediction": bool(prediction),
            "churn_probability": float(probability),
            "customer_data": customer.dict(),
            "features_used": feature_names
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
