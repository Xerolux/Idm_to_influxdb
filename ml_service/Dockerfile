FROM python:3.12-slim

WORKDIR /app

# Copy ML service requirements and install
COPY ml_service/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the idm_logger package (needed for imports)
COPY idm_logger ./idm_logger

# Copy the ml_service code
COPY ml_service .

CMD ["python", "main.py"]
