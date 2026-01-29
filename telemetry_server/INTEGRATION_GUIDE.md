# IDM Telemetry Server Integration Guide

This document outlines the requirements and protocols for clients (data collectors) to integrate with the IDM Telemetry Server. The server collects heat pump telemetry data, aggregates community statistics, and distributes trained anomaly detection models.

## 1. Connection Prerequisites

All communication with the telemetry server must be secure and authenticated.

-   **Base URL:** `https://collector.xerolux.de` (Production)
-   **Protocol:** HTTPS (TLS 1.2+ required). Unencrypted HTTP traffic is rejected.
-   **Authentication:** Bearer Token via HTTP Header.

### Authentication Header
Every sensitive request (data submission, model download, stats retrieval) must include the `Authorization` header:

```http
Authorization: Bearer <YOUR_AUTH_TOKEN>
```

*Note: The token is shared among valid clients. Contact the administrator to obtain the current token.*

## 2. Client Identification (Installation ID)

To ensure data integrity and enable eligibility checks for community models, every client must identify itself with a unique **Installation ID**.

-   **Format:** UUID v4 (e.g., `550e8400-e29b-41d4-a716-446655440000`).
-   **Persistence:** The ID **must be persistent**. It should be generated once upon the first startup of the collector software and stored permanently (e.g., in a config file or database).
-   **Anonymity:** Do not derive this ID from personal data (IP, email). A random UUID is sufficient and preferred.

## 3. Data Ingestion (Telemetry Submission)

Clients should periodically submit collected metrics to the server. Real-time connections are **not** required.

-   **Endpoint:** `POST /api/v1/submit`
-   **Content-Type:** `application/json`

### Batching Strategy

To minimize network traffic and server load, clients are encouraged to buffer data locally and transmit it in larger batches.

*   **Recommended Interval:** Every 1 to 12 hours.
*   **Daily Batching:** Sending data once every 24 hours is perfectly acceptable.
*   **Offline Operation:** The client can operate offline for days and submit the backlog when a connection is available.

The server accepts payloads containing thousands of data points.

### Payload Structure

The payload must be a JSON object with the following schema:

```json
{
  "installation_id": "550e8400-e29b-41d4-a716-446655440000",
  "heatpump_model": "AERO_SLM",
  "version": "1.2.0",
  "data": [
    {
      "timestamp": 1709286000.123,
      "temp_outdoor": 5.4,
      "temp_flow": 32.1,
      "power_compressor": 1200,
      "cop_current": 4.2
    },
    {
      "timestamp": 1709286060.123,
      "temp_outdoor": 5.3,
      "temp_flow": 32.3,
      "power_compressor": 1210,
      "cop_current": 4.1
    },
    "... (up to thousands of records) ..."
  ]
}
```

### Fields

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `installation_id` | UUID | **Yes** | The persistent unique ID of the client installation. |
| `heatpump_model` | String | **Yes** | The model name of the heat pump (e.g., "AERO_SLM"). Used for model-specific training. |
| `version` | String | **Yes** | The version of the data collector software (e.g., "1.2.0"). |
| `data` | List | **Yes** | A list of measurement objects. Can contain records spanning minutes, hours, or days. |

### Measurement Object

Each object in the `data` list represents a snapshot of sensors at a specific time.

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `timestamp` | Float | **Yes** | Unix timestamp (seconds since epoch), ideally with millisecond precision. **Critical:** Must be accurate to when the measurement was *taken*, not when it was sent. |
| `*` | Number/Bool | No | Dynamic metric fields (e.g., `temp_outdoor`, `pressure_high`). Any numeric or boolean field is accepted. |

### Best Practices

1.  **Payload Size:** While the server supports large payloads, try to keep individual requests under **10 MB**. If your 24-hour buffer exceeds this, split it into multiple requests.
2.  **Retry Logic:** If the server returns a `5xx` error, implement an exponential backoff retry strategy. Do **not** retry on `4xx` errors (Client Error), as these indicate invalid data or auth.
3.  **Security:** Ensure the payload does not contain PII (Personally Identifiable Information). The server automatically masks IP addresses.
4.  **Timestamps:** Since data may be sent hours after collection, ensure your local clock is synchronized (NTP) and timestamps are accurate.

## 4. Community Model Access

Clients that contribute data are eligible to download trained anomaly detection models.

### Check Eligibility

Before attempting a download, check if the installation is eligible and if a model update is available.

-   **Endpoint:** `GET /api/v1/model/check`
-   **Query Parameters:**
    -   `installation_id` (Required): The UUID to check.
    -   `model` (Optional): The heat pump model name.
    -   `current_hash` (Optional): The SHA256 hash of the currently installed model (to check for updates).

**Response:**

```json
{
  "eligible": true,
  "reason": "Eligible for community model.",
  "model_available": true,
  "model_hash": "a1b2c3d4...",
  "update_available": true
}
```

### Download Model

-   **Endpoint:** `GET /api/v1/model/download`
-   **Query Parameters:**
    -   `installation_id` (Required): Must match the ID used for data submission.
    -   `model` (Optional): The heat pump model name.
-   **Headers:** `Authorization: Bearer <TOKEN>`

**Response:** Binary file stream (`application/octet-stream`). The file is encrypted and signed.

## 5. Security & Privacy

-   **Transport Security:** All traffic MUST use HTTPS.
-   **IP Masking:** The server automatically masks client IP addresses (e.g., `192.168.xxx.xxx`) in logs to comply with privacy standards (GDPR).
-   **Data Isolation:** Data is aggregated for community statistics. Individual installation data is used for training but never exposed raw to other users.
