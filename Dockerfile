# Dockerfile for LYRA AI
# Multi-stage build for smaller final image

# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash lyra && \
    mkdir -p /home/lyra/app && \
    chown lyra:lyra /home/lyra/app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/lyra/.local

# Make sure scripts in .local are usable
ENV PATH=/home/lyra/.local/bin:$PATH

# Copy application code
COPY . /home/lyra/app
WORKDIR /home/lyra/app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=lyra.api:app \
    FLASK_ENV=production

# Switch to non-root user
USER lyra

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "-m", "lyra", "--api", "--host", "0.0.0.0", "--port", "5000"]
