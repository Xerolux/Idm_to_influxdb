# IDM Telemetry Server Integration Guide

This document outlines the requirements and protocols for clients (data collectors) to integrate with the IDM Telemetry Server. The server collects heat pump telemetry data, aggregates community statistics, and distributes trained anomaly detection models.

**Target Audience:** Developers & AI Agents implementing a client.

## 1. Configuration Checklist

Before starting implementation, ensure you have:

*   [ ] **Server URL:** `https://collector.xerolux.de` (Production)
*   [ ] **Auth Token:** A valid Bearer Token (shared secret).
*   [ ] **Installation ID:** A generated UUID v4 (persistent across restarts).
*   [ ] **Heat Pump Model:** The specific model name (e.g., "AERO_SLM").

## 2. Authentication

*   **Protocol:** HTTPS (TLS 1.2+ required).
*   **Header:** `Authorization: Bearer <YOUR_AUTH_TOKEN>`
*   **Scope:** Required for all endpoints except `/health` and `/api/v1/pool/status`.

## 3. Client Logic Flow (Happy Path)

An AI agent or developer should implement the following state machine:

1.  **Startup:**
    *   Load configuration (Token, URL).
    *   Load or generate (and save) `installation_id` (UUID v4).
2.  **Maintenance (Daily):**
    *   Call `GET /api/v1/model/check` with `installation_id`.
    *   If `eligible` is `true` AND `update_available` is `true`:
        *   Call `GET /api/v1/model/download`.
        *   Save the downloaded `.enc` file locally.
3.  **Data Collection Loop:**
    *   Collect sensor data (every ~60s).
    *   Buffer data locally (RAM or disk).
4.  **Submission (Interval: 1h - 24h):**
    *   Format buffered data into the JSON payload.
    *   Call `POST /api/v1/submit`.
    *   If successful (HTTP 200/204): Clear buffer.
    *   If failed (HTTP 5xx): Keep buffer, retry later (exponential backoff).
    *   If failed (HTTP 4xx): Discard buffer (invalid data), log error.

## 4. Endpoints & Examples

### A. Check Eligibility & Model Status

Check if the client is allowed to download models and if a new model is available.

*   **Method:** `GET`
*   **URL:** `/api/v1/model/check`
*   **Params:** `installation_id` (UUID), `model` (String), `current_hash` (Optional String)

**Request (cURL):**
```bash
curl -X GET "https://collector.xerolux.de/api/v1/model/check?installation_id=550e8400-e29b-41d4-a716-446655440000&model=AERO_SLM" \
     -H "Authorization: Bearer my-secret-token"
```

**Response (JSON):**
```json
{
  "eligible": true,
  "reason": "Eligible for community model.",
  "model_available": true,
  "model_hash": "a1b2c3d4...",
  "update_available": true,
  "model_metadata": {
    "model_name": "AERO_SLM",
    "trained_at": "2024-03-01T03:00:00.123456",
    "samples_processed": 150000,
    "data_points": 2500000,
    "installations": 42
  }
}
```

### B. Download Model

Download the encrypted model file.

*   **Method:** `GET`
*   **URL:** `/api/v1/model/download`
*   **Params:** `installation_id` (UUID), `model` (String)

**Request (cURL):**
```bash
curl -X GET "https://collector.xerolux.de/api/v1/model/download?installation_id=550e8400-e29b-41d4-a716-446655440000&model=AERO_SLM" \
     -H "Authorization: Bearer my-secret-token" \
     -o model.enc
```

**Response:** Binary stream (`application/octet-stream`).

### C. Submit Telemetry Data

Upload buffered data.

*   **Method:** `POST`
*   **URL:** `/api/v1/submit`
*   **Content-Type:** `application/json`

**Request (cURL):**
```bash
curl -X POST "https://collector.xerolux.de/api/v1/submit" \
     -H "Authorization: Bearer my-secret-token" \
     -H "Content-Type: application/json" \
     -d '{
           "installation_id": "550e8400-e29b-41d4-a716-446655440000",
           "heatpump_model": "AERO_SLM",
           "version": "1.2.0",
           "data": [
             {
               "timestamp": 1709286000.123,
               "temp_outdoor": 5.4,
               "temp_flow": 32.1,
               "power_compressor": 1200
             },
             {
               "timestamp": 1709286060.123,
               "temp_outdoor": 5.3,
               "temp_flow": 32.3,
               "power_compressor": 1210
             }
           ]
         }'
```

**Payload Schema:**

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| `installation_id` | UUID | Yes | Must be a valid UUID string. |
| `heatpump_model` | String | Yes | No special characters allowed except `_`, `-`, `.`, `()`. |
| `version` | String | Yes | Client version. |
| `data` | List[Object] | Yes | List of measurements. |

**Measurement Object:**

| Field | Type | Required | Notes |
| :--- | :--- | :--- | :--- |
| `timestamp` | Float | Yes | Unix timestamp (seconds). Critical for reconstruction. |
| `[metric]` | Number/Bool | No | e.g. `temp_outdoor`, `cop_current`. |

## 5. Implementation Notes

*   **UUID Generation:** Use a standard library (e.g., Python `uuid.uuid4()`) on first run. Save it to a file. **Do not** generate a new one on every restart.
*   **Batching:** The server accepts large payloads. Sending 24 hours of minute-resolution data (~1440 records) in one request is the recommended "happy path".
*   **Time Synchronization:** Ensure the client system clock is synchronized (NTP) so timestamps are accurate.
*   **Security:** Mask IPs in logs. Do not send PII in the payload.
