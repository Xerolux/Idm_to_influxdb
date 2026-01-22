# Critical Bug Found: Frontend Outdated!

## Problem

The deployed frontend on `192.168.178.52:5008` is **outdated**!

### Evidence
- **Live frontend**: `index-A39HXyTc.js`
- **Local build**: `index-DUsQpSUB.js`

The deployed version lacks:
- Debug logging for troubleshooting
- "No Data" message when charts are empty
- Loading states
- WebSocket stability fixes
- Proper error handling

## Root Cause

The frontend needs to be rebuilt and redeployed to the Docker container.

## Solution

### Option 1: Rebuild Docker Image (Recommended)
```bash
cd /path/to/idm-metrics-collector
docker build -t ghcr.io/xerolux/idm-metrics-collector:latest .
docker stop idm-logger
docker rm idm-logger
docker run -d --name idm-logger --restart unless-stopped \
  -p 5008:5000 \
  --network idm-network \
  -v /path/to/data:/app/data \
  ghcr.io/xerolux/idm-metrics-collector:latest
```

### Option 2: Quick Fix (Copy Frontend Files)
```bash
# Build frontend locally
cd frontend
npm run build

# Copy to running container
cd ..
docker cp idm_logger/static/ idm-logger:/app/idm_logger/

# Restart container
docker restart idm-logger
```

### Option 3: SSH into Server and Build There
```bash
ssh root@192.168.178.52
cd /path/to/idm-metrics-collector
cd frontend
npm run build
cd ..
docker-compose up -d --build idm-logger
```

## Verification

After redeployment:
1. Open browser to `http://192.168.178.52:5008`
2. Open DevTools (F12) → Console
3. Look for debug logs:
   ```
   [ChartCard] Mounted with props: { title: "...", queriesCount: 3, ... }
   [ChartCard] fetchData called for: ... with 3 queries
   [ChartCard] Data for Aussen: { resultCount: 1, hasValues: true }
   ```
4. Check that charts show "Keine Daten verfügbar" if empty
5. Verify WebSocket connections stay stable

## What Was Fixed in New Build

1. **Debug Logging** - ChartCard now logs:
   - Props on mount
   - fetchData calls
   - API responses
   - Dataset creation

2. **No Data Message** - Shows helpful message when:
   - No queries configured
   - API returns empty results
   - VictoriaMetrics has no data

3. **Loading State** - Shows spinner during data fetch

4. **Better Error Handling** - Warns in console when:
   - Queries array is empty
   - API calls fail
   - Data parsing fails

## Next Steps

After redeploying the frontend, if charts still show no data:
1. Check Console logs for specific error messages
2. Verify VictoriaMetrics has data: `curl "http://192.168.178.52:8428/api/v1/query?query=idm_heatpump_temp_outside"`
3. Check if metrics are being written from Modbus
4. Verify API authentication is working

## Deploy Command

```bash
# On the server (192.168.178.52)
cd /path/to/repo
git pull origin main
cd frontend
npm install
npm run build
cd ..
docker-compose build idm-logger
docker-compose up -d idm-logger
```

This will:
1. Pull latest code with debug improvements
2. Rebuild frontend with fixes
3. Rebuild Docker image
4. Restart container with new frontend
