FROM python:3.14-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install InfluxDB v3 CLI (optional)
# Note: For v3 CLI installation, visit https://docs.influxdata.com/influxdb/v3/reference/cli/

# Copy application
COPY idm_logger/ idm_logger/

# Create data directory for persistent storage (SQLite, secret key)
RUN mkdir -p /app/data
VOLUME /app/data

# Set DATA_DIR environment variable for persistence
ENV DATA_DIR=/app/data
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Health check using Python instead of curl (no extra packages needed)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/health', timeout=5)" || exit 1

CMD ["python", "-m", "idm_logger.logger"]
