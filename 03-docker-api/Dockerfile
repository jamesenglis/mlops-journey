FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create models directory
RUN mkdir -p /app/models

# Copy application code
COPY app/ /app/

# Copy model files
COPY models/ /app/models/

# Debug: List files to verify everything is copied
RUN echo "🔍 Checking Docker container file structure:" && \
    ls -la /app/ && \
    echo "📁 Models directory:" && \
    ls -la /app/models/ && \
    echo "✅ Docker build complete"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
