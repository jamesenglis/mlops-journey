#!/bin/bash
echo "🔍 VERIFYING GITHUB ACTIONS WORKFLOW"

echo "1. Checking file existence..."
if [ -f ".github/workflows/ml-pipeline.yml" ]; then
    echo "✅ Workflow file exists"
else
    echo "❌ Workflow file missing"
    exit 1
fi

echo "2. Checking file size..."
filesize=$(wc -l < .github/workflows/ml-pipeline.yml)
echo "   File has $filesize lines"

echo "3. Checking YAML structure..."
if command -v python &> /dev/null; then
    python -c "
import yaml
try:
    with open('.github/workflows/ml-pipeline.yml', 'r') as f:
        data = yaml.safe_load(f)
    print('✅ YAML syntax is valid')
    print('   Workflow name:', data.get('name', 'Not found'))
    print('   Number of jobs:', len(data.get('jobs', {})))
except Exception as e:
    print(f'❌ YAML error: {e}')
"
else
    echo "ℹ️  Python not available for YAML validation"
fi

echo "4. Checking jobs..."
grep -E "^  [a-zA-Z]" .github/workflows/ml-pipeline.yml

echo "🎉 Workflow verification complete!"
