# Network Access Control (IP Whitelist/Blacklist)

## Overview

The IDM Metrics Collector includes a configurable network access control system to protect your heat pump from unauthorized access. This feature allows you to restrict access based on IP addresses and network ranges using whitelist and blacklist rules.

## Features

- **IP-based Access Control**: Allow or block access based on client IP addresses
- **CIDR Notation Support**: Define entire network ranges (e.g., `192.168.1.0/24`)
- **Whitelist Mode**: Only allow specific IPs/networks (most secure)
- **Blacklist Mode**: Block specific IPs/networks while allowing others
- **Combined Mode**: Use both whitelist and blacklist together
- **Web UI Configuration**: Easy-to-use interface for managing rules
- **Environment Variable Support**: Configure via Docker environment variables

## Configuration

### Via Web UI

1. Navigate to the **Configuration** page
2. Find the **Network Access Control** section
3. Enable the feature by checking **"Enable IP-based Access Control"**
4. Add IP addresses or networks to the whitelist/blacklist (one per line)
5. Click **"Save Configuration"**
6. **Important**: Restart the service for changes to take effect

**Warning**: Make sure your current IP address is in the whitelist before enabling this feature, or you will be locked out!

### Via Environment Variables

Add these to your `docker-compose.yml` or Docker run command:

```yaml
environment:
  - NETWORK_SECURITY_ENABLED=true
  - NETWORK_SECURITY_WHITELIST=192.168.1.0/24,10.0.0.5
  - NETWORK_SECURITY_BLACKLIST=203.0.113.0/24
```

**Format**: Comma-separated list of IP addresses or CIDR networks.

### Via Configuration File (Advanced)

The settings are stored in the database under the `network_security` section:

```json
{
  "network_security": {
    "enabled": true,
    "whitelist": [
      "192.168.1.0/24",
      "10.0.0.5"
    ],
    "blacklist": [
      "203.0.113.0/24"
    ]
  }
}
```

## How It Works

### Access Control Logic

1. **Disabled Mode**: If `enabled: false`, all IPs are allowed (default)

2. **Blacklist Check** (happens first):
   - If client IP matches any blacklist entry → **Access Denied (403)**
   - Blacklist has priority over whitelist

3. **Whitelist Check**:
   - If whitelist is **empty** → All IPs allowed (unless blacklisted)
   - If whitelist is **not empty**:
     - Client IP matches whitelist entry → **Access Allowed**
     - Client IP does NOT match → **Access Denied (403)**

### Examples

#### Example 1: Whitelist Only (Most Secure)
Allow only your local network:

```
Whitelist:
192.168.1.0/24

Blacklist:
(empty)
```

**Result**:
- ✅ `192.168.1.100` → Allowed
- ✅ `192.168.1.1` → Allowed
- ❌ `10.0.0.5` → Blocked
- ❌ `203.0.113.5` → Blocked

#### Example 2: Blacklist Only
Block known malicious networks, allow everything else:

```
Whitelist:
(empty)

Blacklist:
203.0.113.0/24
198.51.100.0/24
```

**Result**:
- ✅ `192.168.1.100` → Allowed
- ✅ `10.0.0.5` → Allowed
- ❌ `203.0.113.50` → Blocked
- ❌ `198.51.100.20` → Blocked

#### Example 3: Combined Mode
Allow local networks, but block specific troublesome IP:

```
Whitelist:
192.168.1.0/24
10.0.0.0/24

Blacklist:
192.168.1.50
```

**Result**:
- ✅ `192.168.1.100` → Allowed
- ❌ `192.168.1.50` → Blocked (blacklist has priority)
- ✅ `10.0.0.5` → Allowed
- ❌ `172.16.0.1` → Blocked (not in whitelist)

## CIDR Notation Reference

Common network ranges:

| CIDR Notation | IP Range | Number of IPs | Use Case |
|---------------|----------|---------------|----------|
| `192.168.1.1/32` | Single IP | 1 | Specific device |
| `192.168.1.0/30` | .0 - .3 | 4 | Very small network |
| `192.168.1.0/24` | .0 - .255 | 256 | Home network |
| `192.168.0.0/16` | .0.0 - .255.255 | 65,536 | Large private network |
| `10.0.0.0/8` | All 10.x.x.x | 16,777,216 | Entire Class A private |
| `172.16.0.0/12` | 172.16-31.x.x | 1,048,576 | Class B private range |

**Online Calculator**: Use https://www.ipaddressg uide.com/cidr to calculate CIDR ranges.

## Security Best Practices

### 1. Use Whitelist Mode for Production
The most secure approach is to only allow known good IPs:

```
Whitelist:
- Your home network: 192.168.1.0/24
- Your VPN: 10.8.0.0/24
- Your mobile network: (get from your provider)

Blacklist: (empty)
```

### 2. Always Include Your Current IP
Before enabling the feature:
1. Check "Your current IP" shown in the Web UI
2. Add it to the whitelist
3. Then enable the feature

### 3. Test Before Applying
If possible, test the configuration on a non-critical system first.

### 4. Keep a Backup Access Method
- Configure VPN access as a backup
- Have console access to the Docker host
- Keep SSH access to the server unrestricted

### 5. Monitor Logs
Check logs for blocked access attempts:

```bash
docker logs idm-logger | grep "Blocked IP"
```

## Troubleshooting

### Locked Out of Web UI

**Symptom**: You get a 403 Forbidden error when accessing the web interface.

**Solutions**:

1. **Via Docker Shell**:
   ```bash
   docker exec -it idm-logger python3 -c "
   from idm_logger.config import config
   config.data['network_security']['enabled'] = False
   config.save()
   print('Network security disabled')
   "
   docker restart idm-logger
   ```

2. **Via Environment Variable**:
   Add to `docker-compose.yml`:
   ```yaml
   environment:
     - NETWORK_SECURITY_ENABLED=false
   ```
   Then: `docker-compose up -d`

3. **Via Database**:
   ```bash
   docker exec -it idm-logger python3 -c "
   from idm_logger.db import db
   import json
   cfg = json.loads(db.get_setting('config'))
   cfg['network_security']['enabled'] = False
   db.set_setting('config', json.dumps(cfg))
   "
   ```

### Access Still Blocked After Disabling

- Restart the service: `docker restart idm-logger`
- Clear browser cache and cookies
- Try from a different browser or incognito mode

### Whitelist Not Working

- Verify CIDR notation is correct
- Check that your IP hasn't changed (DHCP)
- Ensure no typos in IP addresses
- Check that the service was restarted after changes

### How to Find Your Public IP

If accessing from the Internet:
- Visit: https://whatismyipaddress.com
- Or run: `curl ifconfig.me`

If accessing from local network:
- Windows: `ipconfig`
- Linux/Mac: `ip addr` or `ifconfig`

## API Reference

### Get Current Configuration

```bash
GET /api/config

Response:
{
  "network_security": {
    "enabled": true,
    "whitelist": ["192.168.1.0/24"],
    "blacklist": []
  }
}
```

### Update Configuration

```bash
POST /api/config

Body:
{
  "network_security_enabled": true,
  "network_security_whitelist": "192.168.1.0/24\n10.0.0.5",
  "network_security_blacklist": "203.0.113.0/24"
}
```

Note: Whitelist and blacklist are newline-separated strings in the API.

## Technical Details

### Implementation

- **Middleware**: Flask `@app.before_request` hook
- **IP Parsing**: Python `ipaddress` library
- **Priority**: Blacklist checked before whitelist
- **Performance**: Negligible overhead (<1ms per request)

### Compatibility

- IPv4: Full support
- IPv6: Full support (use IPv6 CIDR notation)
- Proxy Support: Uses `request.remote_addr` (configure proxy headers if behind reverse proxy)

### Reverse Proxy Configuration

If behind nginx/Apache, configure to pass real IP:

**Nginx**:
```nginx
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

**Note**: You may need to update Flask to use `request.headers.get('X-Real-IP')` or `request.headers.get('X-Forwarded-For')`.

## Support

For issues or questions:
- GitHub Issues: https://github.com/Xerolux/idm-metrics-collector/issues
- Check logs: `docker logs idm-logger`
