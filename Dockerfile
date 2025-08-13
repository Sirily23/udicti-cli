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

# Create a non-root user
RUN useradd --create-home --shell /bin/bash udicti
USER udicti

# For background worker - keep container alive
CMD ["tail", "-f", "/dev/null"]