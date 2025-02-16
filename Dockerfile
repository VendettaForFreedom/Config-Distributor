# Use Python 3.13.2 slim image
FROM python:3.13.2-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories and files
RUN mkdir -p teletweet && \
    touch teletweet/tags.txt

# Environment variables will be provided through docker-compose or docker run
ENV PYTHONPATH=/app

# Run the bot
CMD ["python", "-m", "teletweet.tweetbot"]
