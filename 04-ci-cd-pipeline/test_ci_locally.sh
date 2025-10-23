#!/bin/bash

echo "🚀 Testing CI Pipeline Locally"

echo "1. Checking project structure..."
echo "   Current directory: $(pwd)"
echo "   Files:"
ls -la

echo "2. Testing Python imports..."
python -c "import pytest; print('✅ pytest available')"
python -c "import pandas; print('✅ pandas available')"
python -c "import sklearn; print('✅ sklearn available')"

echo "3. Running tests..."
python -m pytest tests/ -v

echo "4. Checking workflow file..."
if [ -f ".github/workflows/ml-pipeline.yml" ]; then
    echo "✅ GitHub Actions workflow ready"
    echo "   Jobs: test, build-and-test-api, security-scan, deploy-staging, deploy-production"
else
    echo "❌ Workflow file missing"
fi

echo "✅ Local CI test completed!"
