## 2024-05-22 - Unauthenticated Internal Endpoint Exposure

**Vulnerability:** The `/api/internal/ml_alert` endpoint was exposed without authentication, intended only for internal service communication but reachable via exposed ports.
**Learning:** Reliance on network isolation (e.g., "internal" Docker networks) is insufficient when services also map ports to the host (e.g., `5008:5000`). "Internal" endpoints become public if not explicitly protected.
**Prevention:** Always implement application-level authentication (e.g., Shared API Keys, mTLS) for service-to-service communication, regardless of network architecture.
