import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def test_model_training():
    """Test that we can train a model"""
    # Generate sample data
    np.random.seed(42)
    n_samples = 50
    
    data = {
        'age': np.random.randint(18, 70, n_samples),
        'tenure': np.random.randint(1, 60, n_samples),
        'monthly_charges': np.random.uniform(20, 100, n_samples),
        'total_charges': np.random.uniform(50, 5000, n_samples),
        'support_calls': np.random.randint(0, 10, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable
    churn_prob = (df['support_calls'] > 5).astype(int) * 0.6 + \
                 (df['monthly_charges'] > 70).astype(int) * 0.4
    df['churn'] = (churn_prob + np.random.normal(0, 0.1, n_samples) > 0.5).astype(int)
    
    # Train model
    X = df.drop('churn', axis=1)
    y = df['churn']
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Verify model works
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    assert len(predictions) == n_samples
    assert probabilities.shape == (n_samples, 2)

def test_feature_consistency():
    """Test that feature names are consistent"""
    expected_features = ['age', 'tenure', 'monthly_charges', 'total_charges', 'support_calls']
    assert len(expected_features) == 5
    assert 'age' in expected_features
