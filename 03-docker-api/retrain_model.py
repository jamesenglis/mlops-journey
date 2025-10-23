import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

print("🔄 Retraining model with current environment...")

# Generate sample data
np.random.seed(42)
n_samples = 1000

data = {
    'age': np.random.randint(18, 70, n_samples),
    'tenure': np.random.randint(1, 60, n_samples),
    'monthly_charges': np.random.uniform(20, 100, n_samples),
    'total_charges': np.random.uniform(50, 5000, n_samples),
    'contract_type': np.random.choice(['Monthly', 'Yearly', 'Two-year'], n_samples),
    'support_calls': np.random.randint(0, 10, n_samples)
}

df = pd.DataFrame(data)

# Create target variable
churn_prob = (df['support_calls'] > 5).astype(int) * 0.6 + \
             (df['monthly_charges'] > 70).astype(int) * 0.4
df['churn'] = (churn_prob + np.random.normal(0, 0.1, n_samples) > 0.5).astype(int)

# Preprocess data
df_processed = pd.get_dummies(df, columns=['contract_type'])

X = df_processed.drop('churn', axis=1)
y = df_processed['churn']

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model and feature names
joblib.dump(model, 'models/churn_predictor.pkl')
joblib.dump(list(X.columns), 'models/feature_names.pkl')

print("✅ Model retrained and saved successfully!")
print(f"Feature names: {list(X.columns)}")
print(f"Model score: {model.score(X, y):.3f}")
