# Use lightweight Python
FROM python:3.10-slim

# Prevent Python buffering (logs show instantly)
ENV PYTHONUNBUFFERED=1

# Fix pip timeout issues
ENV PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Install system deps (IMPORTANT for faiss + torch)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python deps
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
