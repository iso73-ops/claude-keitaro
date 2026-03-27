---
name: keitaro-flows
description: >
  Manage Keitaro streams/flows: create, update, configure filters, set weights,
  A/B test landings and offers, setup cloaking patterns. Use when user says
  "flow", "stream", "weight", "filter", "A/B test", "split test", "cloaking",
  "white page", or "traffic distribution".
---

# Keitaro Flow Management

## Process

1. Read `keitaro/references/keitaro-api.md` for stream endpoint details
2. Read `keitaro/references/flow-patterns.md` for common patterns
3. Parse user intent and context
4. Execute API calls
5. Display result

## Create Flow

When user describes a flow setup:

1. Identify the pattern (see `references/flow-patterns.md`):
   - White + Offer (cloaking)
   - A/B test
   - GEO split
   - Device split
   - Direct offer
2. Determine required fields:
   - Campaign ID (required)
   - Type: regular, forced, or default
   - Schema: redirect, landings, offers, or landings_offers
   - Weight (for A/B testing)
   - Filters (geo, device, OS, etc.)
   - Landing page IDs
   - Offer IDs
3. Create via API

### Quick Patterns

**"Add white page to campaign 12":**
```json
{
  "campaign_id": 12,
  "type": "default",
  "name": "White Page",
  "schema": "landings",
  "landing_page_ids": [<white_landing_id>]
}
```

**"Add offer flow for DE desktop":**
```json
{
  "campaign_id": 12,
  "type": "regular",
  "name": "DE Desktop",
  "weight": 100,
  "schema": "landings_offers",
  "filters": [
    {"name": "geo", "mode": "accept", "payload": "DE"},
    {"name": "device_type", "mode": "accept", "payload": "desktop"}
  ],
  "landing_page_ids": [5, 6],
  "offer_ids": [10]
}
```

## Update Weights

When user says "change weights" or "rebalance":

1. List current flows with weights
2. Show current distribution
3. Apply new weights
4. Confirm changes

Example: "set flow A to 70% and flow B to 30%"

## Configure Filters

Supported filters (from API):
- `geo` — country codes
- `region`, `city` — location
- `device_type` — desktop, mobile, tablet
- `os` — Windows, macOS, iOS, Android
- `browser` — Chrome, Firefox, Safari
- `language` — browser language
- `connection_type` — wifi, cellular
- `ip` — IP ranges
- `referrer` — referrer URL pattern
- `sub_id_1` through `sub_id_15` — sub-ID values

## A/B Test Setup

When user says "A/B test landings in campaign 12":

1. Get current campaign flows
2. Create separate flows with equal weights
3. Assign different landings to each flow
4. Confirm setup with summary:

```
A/B Test Created:
├── Flow A: landing_v1.html (50% weight)
├── Flow B: landing_v2.html (50% weight)
└── Min. data needed: 100 clicks per variant
```

## Cloaking Setup

When user says "setup cloaking for campaign 12":

1. Create default flow with white page
2. Create regular flow(s) with:
   - GEO filter (target countries)
   - Referrer filter (traffic source domain)
   - Device filter if needed
3. Assign offer landings to regular flows
4. Show complete setup summary

## Flow Health Check

Quick checks for a campaign's flows:
- Any flows with 0 clicks in 24h? → "Not receiving traffic"
- Any flows with weight 0? → "Effectively disabled"
- Default flow missing? → "No white page, risky for paid traffic"
- Filters contradicting each other? → "Conflicting filters"
