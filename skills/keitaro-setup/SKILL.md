---
name: keitaro-setup
description: >
  Keitaro API connection setup and verification. Configures KEITARO_URL and
  KEITARO_API_KEY, tests connection, shows tracker status. Use when user says
  "setup", "connect", "configure keitaro", "API key", or first-time setup.
---

# Keitaro Setup

## Process

1. Ask user for their Keitaro tracker URL (e.g. https://tracker.example.com)
2. Ask for API key (found in Account → API keys in Keitaro dashboard)
3. Test connection by calling `GET /campaigns` via the API helper
4. If successful, show tracker status (number of campaigns, domains, etc.)
5. Save config for session

## Connection Test

Run the API helper to verify connection:

```bash
KEITARO_URL="<user-url>" KEITARO_API_KEY="<user-key>" \
  python3 ~/.claude/skills/keitaro/scripts/keitaro_api.py test
```

## Expected Output on Success

```
Connection successful!
Tracker: https://tracker.example.com
Campaigns: 15 active, 3 archived
Domains: 5 active
Offers: 23 active
```

## If Connection Fails

Common issues:
1. **401 Unauthorized** — wrong API key. Check Account → API keys
2. **Connection refused** — wrong URL or tracker is down
3. **SSL error** — tracker uses self-signed cert or HTTP instead of HTTPS
4. **404** — URL path is wrong, ensure no trailing slash

## Environment Variables

After successful connection, remind user to set in their shell profile:

```bash
export KEITARO_URL="https://tracker.example.com"
export KEITARO_API_KEY="your-api-key-here"
```

Or in Claude Code settings for persistent use across sessions.

## Security Note

- Never display the full API key — show only first 4 and last 4 characters
- Never commit API keys to files
- Recommend using environment variables, not hardcoded values
