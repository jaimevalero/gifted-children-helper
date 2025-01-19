FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PYTHONPATH=/app:/app/gifted_children_helper_backend

WORKDIR /app


# Install additional packages from packages.txt
COPY packages.txt .
RUN apt-get update \
    && xargs -a packages.txt apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure .env exists
RUN touch .env

EXPOSE $PORT

CMD ["sh", "-c", "source /app/.env 2>/dev/null || true && exec uvicorn gifted_children_helper_backend.backend_fastapi.main:app --host 0.0.0.0 --port ${PORT}"]
