# Week 3: Docker & API Deployment

## 🚀 Project Overview
Successfully deployed customer churn prediction model as a FastAPI web service with automatic documentation.

## ✅ API Endpoints Working
- \`GET /\` - API information ✅
- \`GET /health\` - Health check ✅  
- \`GET /predict/{user_id}\` - Single predictions ✅
- \`POST /predict/batch\` - Batch predictions ✅

## 📊 Model Performance
- **Accuracy**: High precision predictions
- **Features**: 11 engineered features from SQL data
- **Business Value**: Identifies at-risk customers with actionable recommendations

## 🛠️ Technical Stack
- FastAPI with automatic Swagger documentation
- SQLite database integration
- Scikit-learn Random Forest model
- Joblib model serialization
- Real-time predictions

## 🌐 Access
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 Example Prediction
\`\`\`json
{
  "user_id": 1,
  "churn_probability": 0.43,
  "will_churn": false,
  "risk_level": "MEDIUM",
  "recommendation": "Continue normal engagement",
  "status": "success"
}
\`\`\`

## 🚀 Quick Start
\`\`\`bash
cd app
python main.py
\`\`\`

*Part of the 30-Day MLOps Journey - Building production ML systems from scratch*
