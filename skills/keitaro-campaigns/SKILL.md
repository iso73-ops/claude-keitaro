---
name: keitaro-campaigns
description: >
  Create, list, update, delete, enable, disable, and clone Keitaro campaigns
  via natural language. Use when user says "create campaign", "new campaign",
  "list campaigns", "disable campaign", "clone campaign", or describes a
  campaign setup.
---

# Keitaro Campaign Management

## Process

1. Read `keitaro/references/keitaro-api.md` for campaign endpoint details
2. Parse user intent (create, list, update, delete, enable, disable, clone)
3. Collect required fields from user context
4. Execute API call via helper script
5. Display result in clean format

## Create Campaign

When user says "create campaign for [vertical] [GEO]":

1. Generate campaign name: `{vertical}_{geo}_{date}` (e.g. `gambling_de_20260327`)
2. Generate alias: lowercase, no spaces (e.g. `gambling-de-1`)
3. Ask user for missing required info:
   - Traffic source (Facebook, Google, TikTok, Push, etc.)
   - Domain to use (list available domains first)
   - Cost model (CPC/CPM/CPA) and cost value
4. Create campaign via API
5. Show result with campaign URL

```bash
python3 ~/.claude/skills/keitaro/scripts/keitaro_api.py campaign create \
  --name "gambling_de_20260327" \
  --alias "gambling-de-1" \
  --domain-id 1 \
  --traffic-source-id 5
```

## List Campaigns

Show campaigns in table format:

```
| ID | Name | State | Clicks | Conv | ROI | Updated |
|----|------|-------|--------|------|-----|---------|
| 12 | gambling_de | active | 5,432 | 89 | 23% | 2h ago |
| 15 | crypto_at | active | 1,203 | 12 | -8% | 5h ago |
| 18 | nutra_br | disabled | 890 | 45 | 41% | 1d ago |
```

## Update Campaign

Parse what user wants to change:
- "rename campaign 12 to ..." → PUT with new name
- "change cost to $0.05 CPC" → PUT with cost_type + cost_value
- "move campaign 12 to group X" → PUT with group_id

## Disable/Enable Campaign

Quick actions:
- "pause campaign 12" → POST `/campaigns/12/disable`
- "start campaign 12" → POST `/campaigns/12/enable`
- "pause all gambling campaigns" → iterate and disable each (with confirmation)

## Clone Campaign

- "clone campaign 12" → POST `/campaigns/12/clone`
- "clone campaign 12 for AT" → clone + update GEO filters in flows

## Delete Campaign

**Always require explicit confirmation before deletion.**

- "delete campaign 12" → Warn about permanent data loss
- "archive campaign 12" → DELETE (soft delete, can restore)

## Bulk Operations

When user asks about multiple campaigns:
- "pause all campaigns with ROI < -30%" → build report first, show list, confirm, then disable each
- Always show what will be affected before executing
- Max batch: process 20 campaigns at a time to avoid timeouts
