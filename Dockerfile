# Use Debian as base image
FROM debian:bullseye-slim

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Add deadsnakes PPA and install Python 3.10
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    software-properties-common \
    && echo "deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu focal main" > /etc/apt/sources.list.d/deadsnakes-ubuntu-ppa.list \
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 \
    && apt-get update \
    && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-distutils \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install additional packages listed in packages.txt
COPY packages.txt .
RUN apt-get update && xargs -a packages.txt apt-get install -y && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy only the requirements first to leverage Docker cache
COPY requirements.txt .

# Create and activate virtual environment
RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variables
ENV PORT=8000 \
    PYTHONPATH=/app:/app/gifted_children_helper_backend

# Expose the port
EXPOSE $PORT

# Start FastAPI application
CMD ["sh", "-c", "uvicorn gifted_children_helper_backend.backend_fastapi.main:app --host 0.0.0.0 --port ${PORT}"]
