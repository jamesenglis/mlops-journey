# Week 2: Machine Learning Basics - Customer Churn Prediction

## 🎯 Project Overview
Built a complete ML pipeline to predict customer churn using e-commerce data from Week 1's SQL database. The system identifies customers at risk of leaving and provides actionable business recommendations.

## 📊 Model Performance
- **Algorithm**: Random Forest Classifier
- **Accuracy**: High precision on test data
- **Features**: 11 engineered features from SQL data
- **Evaluation**: Classification reports and feature importance analysis

## 🔮 Prediction Results
- **2 customers** identified as low risk (will stay)
- **3 customers** identified as high risk (will churn) 
- **Business recommendations** provided for each customer
- **Churn probabilities** ranging from 28% to 95%

## 🛠️ Technical Stack
- **Python** with scikit-learn, pandas, numpy
- **SQLite** database from Week 1
- **Feature Engineering** from raw SQL data
- **Model Serialization** with joblib
- **Random Forest** classification

## 📁 Project Structure