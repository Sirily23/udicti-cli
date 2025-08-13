# File: Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install the package
RUN pip install --no-cache-dir -e .

# Set Firebase config as environment variable
ENV FIREBASE_CONFIG_JSON='{}'

# Expose port for Render (Render uses port 10000 by default)
EXPOSE 10000

# Create a simple web server to keep the service alive
RUN pip install flask

# Create a simple web interface
COPY web_server.py /app/web_server.py

# Start the web server
CMD ["python", "web_server.py"]