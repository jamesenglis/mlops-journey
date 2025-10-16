# test_api.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing ML API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✅ Health: {response.json()}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return
    
    # Test root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(BASE_URL)
        print(f"   ✅ Root: {response.json()}")
    except Exception as e:
        print(f"   ❌ Root endpoint failed: {e}")
        return
    
    # Test single prediction
    print("\n3. Testing single prediction...")
    try:
        response = requests.get(f"{BASE_URL}/predict/1")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Prediction for user 1:")
            print(f"      Churn Probability: {result['churn_probability']}")
            print(f"      Will Churn: {result['will_churn']}")
            print(f"      Risk Level: {result['risk_level']}")
            print(f"      Recommendation: {result['recommendation']}")
        else:
            print(f"   ❌ Prediction failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Single prediction failed: {e}")
    
    # Test batch prediction
    print("\n4. Testing batch prediction...")
    try:
        customer_ids = [1, 2, 3, 4, 5]
        response = requests.post(
            f"{BASE_URL}/predict/batch",
            json=customer_ids
        )
        if response.status_code == 200:
            results = response.json()
            print(f"   ✅ Batch processed: {results['total_processed']} customers")
            for pred in results['predictions']:
                if 'churn_probability' in pred:
                    print(f"      User {pred['user_id']}: {pred['churn_probability']} probability")
                else:
                    print(f"      User {pred['user_id']}: {pred['error']}")
        else:
            print(f"   ❌ Batch prediction failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Batch prediction failed: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_api()