#!/bin/bash
echo "🧪 COMPREHENSIVE API TEST"

echo "1. Testing health endpoint:"
curl -s http://localhost:8000/health | python -m json.tool

echo -e "
2. Testing debug endpoint:"
curl -s http://localhost:8000/debug | python -m json.tool

echo -e "
3. Testing prediction:"
curl -s -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "tenure": 24,
    "monthly_charges": 75.50,
    "total_charges": 1800.00,
    "contract_type": "Monthly",
    "support_calls": 3
  }' | python -m json.tool

echo -e "
✅ Test completed!"
