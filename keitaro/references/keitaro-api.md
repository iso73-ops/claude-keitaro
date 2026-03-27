# Keitaro Admin API v1 Reference

## Authentication

```
Header: Api-Key: <your-api-key>
Alt:     Authorization: Bearer <your-api-key>
Base:    https://{tracker-domain}/admin_api/v1
```

Keys: Account → API keys in tracker dashboard.

## HTTP Methods

| Method | Purpose |
|--------|---------|
| GET | Retrieve data |
| POST | Create entities, build reports |
| PUT | Update (only specified fields change) |
| DELETE | Archive (soft delete) |

## Batch Requests

Combine multiple requests: append `?batch` or `?bulk` to endpoint.

---

## Campaigns

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/campaigns` | List all campaigns (params: offset, limit) |
| POST | `/campaigns` | Create campaign (required: name, alias) |
| GET | `/campaigns/{id}` | Get campaign details |
| PUT | `/campaigns/{id}` | Update campaign |
| DELETE | `/campaigns/{id}` | Archive campaign |
| POST | `/campaigns/{id}/clone` | Clone campaign |
| POST | `/campaigns/{id}/disable` | Disable campaign |
| POST | `/campaigns/{id}/enable` | Enable campaign |
| POST | `/campaigns/{id}/restore` | Restore archived campaign |
| GET | `/campaigns/{id}/streams` | Get campaign flows/streams |
| POST | `/campaigns/{id}/update_costs` | Update costs (SLOW — async job) |
| POST | `/campaigns/clean_archive` | Permanently delete archived |
| GET | `/campaigns/deleted` | List archived campaigns |

### Campaign Create Fields
- `name` (string, required) — campaign name
- `alias` (string, required) — URL alias (e.g. "cloudservers" → `example.com/cloudservers`)
- `type` (string) — rotation mode: "position" (sequential) or "weight" (random by weight)
- `state` (string) — "active", "disabled"
- `cost_type` (string) — "CPC", "CPuC" (per unique click), "CPM", "CPA", "CPS", "RevShare"
- `cost_value` (number) — cost amount
- `cost_currency` (string) — "USD", "EUR", etc.
- `cost_auto` (boolean) — auto-pull costs from traffic source
- `traffic_loss` (number) — % of traffic lost between source and tracker (adjusts cost)
- `group_id` (integer) — group for organization
- `bind_visitors` (string) — visitor binding mode (weight-based campaigns only):
  - "flow" — bind to same flow
  - "flow_landing" — bind to same flow + landing
  - "flow_landing_offer" — bind to same flow + landing + offer
- `bind_visitors_ttl` (integer) — binding duration in hours (1-8760, default 24)
- `uniqueness_method` (string) — "ip", "ip_ua", "cookies", "get_parameter"
- `uniqueness_ttl` (integer) — uniqueness TTL in hours (1-8760)
- `traffic_source_id` (integer) — linked traffic source
- `domain_id` (integer) — tracker domain to use
- `parameters` (object) — custom sub-id parameters mapping (UTM, sub_id_1-15)
- `token` (string, read-only) — API token for Click API integration

---

## Streams (Flows)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/streams` | List all streams |
| POST | `/streams` | Create stream |
| GET | `/streams/{id}` | Get stream details |
| PUT | `/streams/{id}` | Update stream |
| DELETE | `/streams/{id}` | Delete stream |
| POST | `/streams/{id}/clone` | Clone stream |
| POST | `/streams/{id}/disable` | Disable stream |
| POST | `/streams/{id}/enable` | Enable stream |
| GET | `/campaigns/{id}/streams` | Get streams for campaign |

### Stream Create Fields
- `campaign_id` (integer, required) — parent campaign
- `type` (string) — "regular", "forced", "default"
- `name` (string) — stream name
- `position` (integer) — sort order
- `weight` (integer) — traffic weight (for A/B split)
- `state` (string) — "active", "disabled"
- `action_type` (string) — "redirect", "show_html", "show_landing_page", "none"
- `action_payload` (string) — URL for redirect or HTML content
- `schema` (string) — "redirect", "landings", "landings_offers", "offers"
- `collect_clicks` (boolean) — track clicks
- `filter_or` (boolean) — OR logic for filters (default AND)
- `filters` (array) — traffic filters (geo, device, OS, etc.)
- `landing_page_ids` (array of int) — linked landing pages
- `offer_ids` (array of int) — linked offers
- `triggers` (array) — automation triggers

### Filter Object
```json
{
  "name": "geo",
  "mode": "accept",
  "payload": "DE,AT,CH"
}
```

Common filters:
- `geo` — country codes (DE, US, GB...)
- `region` — region/state
- `city` — city name
- `device_type` — desktop, mobile, tablet
- `os` — Windows, macOS, iOS, Android
- `browser` — Chrome, Firefox, Safari
- `language` — browser language
- `connection_type` — wifi, cellular
- `ip` — IP ranges
- `referrer` — referrer URL pattern
- `uniqueness` — first-time vs. returning visitors
- `limit` — intercept first X clicks only
- `sub_id_*` — sub-id values (sub_id_1 through sub_id_15)

### Stream Processing Order
1. **Forced flows** — evaluated first, top to bottom (bypass regular rotation)
2. **Regular flows** — position-based (sequential) or weight-based (random with binding)
3. **Default flow** — fallback when no other flow matches
4. If no default flow → "Do Nothing" action

### Bulk Stream Operations
- Delete (archive), Clone, Replace (substring in URLs), Equalize (reset weights)
- Favorite flows: save as reusable templates across campaigns (creates clone, not reference)

---

## Landing Pages

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/landing_pages` | List all landings |
| POST | `/landing_pages` | Create landing page |
| GET | `/landing_pages/{id}` | Get landing details |
| PUT | `/landing_pages/{id}` | Update landing |
| DELETE | `/landing_pages/{id}` | Archive landing |
| PUT | `/landing_pages/{id}/clone` | Clone landing |
| POST | `/landing_pages/{id}/add_file` | Upload file (param: path) |
| GET | `/landing_pages/{id}/download` | Download landing files |

### Landing Create Fields
- `name` (string, required) — landing name
- `url` (string) — URL for redirect-type landings
- `action_type` (string) — "redirect", "local_file", "html"
- `action_payload` (string) — HTML content or file path
- `group_id` (integer) — group
- `offer_id` (integer) — default offer for this landing

---

## Offers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/offers` | List all offers |
| POST | `/offers` | Create offer |
| GET | `/offers/{id}` | Get offer details |
| PUT | `/offers/{id}` | Update offer |
| DELETE | `/offers/{id}` | Archive offer |
| POST | `/offers/{id}/clone` | Clone offer |
| POST | `/offers/{id}/restore` | Restore offer |
| GET | `/offers/deleted` | List archived offers |

### Offer Create Fields
- `name` (string, required) — offer name
- `url` (string, required) — offer URL (with macros)
- `affiliate_network_id` (integer) — linked network
- `group_id` (integer) — group
- `payout_type` (string) — "CPA", "CPS", "CPL", "RevShare"
- `payout_value` (number) — payout amount
- `payout_currency` (string) — currency code
- `payout_auto` (boolean) — auto from postback

---

## Affiliate Networks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/affiliate_networks` | List all networks |
| POST | `/affiliate_networks` | Create network |
| GET | `/affiliate_networks/{id}` | Get network details |
| PUT | `/affiliate_networks/{id}` | Update network |
| DELETE | `/affiliate_networks/{id}` | Archive network |
| POST | `/affiliate_networks/{id}/clone` | Clone network |
| POST | `/affiliate_networks/{id}/restore` | Restore network |

### Network Fields
- `name` (string, required) — network name
- `postback_url` (string) — S2S postback URL
- `offer_param` (string) — offer ID parameter name

---

## Traffic Sources

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/traffic_sources` | List all sources |
| POST | `/traffic_sources` | Create source |
| GET | `/traffic_sources/{id}` | Get source details |
| PUT | `/traffic_sources/{id}` | Update source |
| DELETE | `/traffic_sources/{id}` | Archive source |

### Traffic Source Fields
- `name` (string, required) — source name
- `postback_url` (string) — postback URL to send conversions
- `postback_statuses` (array) — which statuses trigger postback
- `template_name` (string) — predefined template (facebook, google, tiktok, etc.)
- `parameters` (array) — parameter mapping for sub-ids

---

## Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/report/build` | Build custom report |

### Report Request
```json
{
  "range": {
    "from": "2026-03-01",
    "to": "2026-03-27",
    "timezone": "Europe/Berlin"
  },
  "columns": [],
  "metrics": ["clicks", "campaign_unique_clicks", "conversions", "revenue", "cost", "profit", "roi", "cr", "epc"],
  "grouping": ["campaign_id"],
  "filters": [
    {"name": "campaign_id", "operator": "EQUALS", "expression": "123"}
  ],
  "sort": [{"name": "profit", "order": "desc"}],
  "summary": true,
  "offset": 0,
  "limit": 100
}
```

### Available Metrics
- `clicks` — total clicks
- `campaign_unique_clicks` — unique clicks
- `conversions` — total conversions
- `revenue` — total revenue
- `cost` — total cost
- `profit` — revenue - cost
- `roi` — return on investment %
- `cr` — conversion rate %
- `epc` — earnings per click
- `ecpm` — earnings per 1000 impressions
- `cpc` — cost per click
- `cpa` — cost per action

### Grouping Options
- `campaign_id`, `stream_id`, `landing_page_id`, `offer_id`
- `affiliate_network_id`, `traffic_source_id`
- `country`, `region`, `city`
- `device_type`, `os`, `browser`
- `connection_type`, `isp`
- `sub_id_1` through `sub_id_15`
- `day`, `week`, `month`, `hour`
- `datetime` — full datetime grouping

### Filter Operators
- `EQUALS`, `NOT_EQUALS`
- `CONTAINS`, `NOT_CONTAINS`
- `GREATER`, `LESS`
- `IN_LIST`, `NOT_IN_LIST`
- `EMPTY`, `NOT_EMPTY`

---

## Clicks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/clicks/log` | Get click log with details |
| POST | `/clicks/clean` | Clean click stats (date range) |
| POST | `/clicks/update_costs` | Bulk update costs |

---

## Conversions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/conversions/log` | Get conversion log |

### Conversion Log Request
```json
{
  "columns": ["datetime", "campaign_id", "stream_id", "sub_id_1", "revenue", "status"],
  "filters": [],
  "range": {"from": "2026-03-01", "to": "2026-03-27", "timezone": "UTC"},
  "order": [{"name": "datetime", "order": "desc"}],
  "offset": 0,
  "limit": 100
}
```

---

## Domains

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/domains` | List domains |
| POST | `/domains` | Create domain (required: name) |
| GET | `/domains/{id}` | Get domain details |
| PUT | `/domains/{id}` | Update domain |
| DELETE | `/domains/{id}` | Archive domain |
| POST | `/domains/{id}/check` | Check domain status/DNS |
| POST | `/domains/{id}/restore` | Restore domain |
| GET | `/domains/ip` | Get server IP (ipv4, ipv6) |
| POST | `/domains/register` | Register domain (Namecheap) |

---

## Groups

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/groups?type=campaigns` | List groups (type: campaigns/offers/landings/domains) |
| POST | `/groups` | Create group (required: name, position, type) |
| PUT | `/groups/{id}` | Update group |
| DELETE | `/groups/{id}/delete` | Delete group |

---

## Bot List

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/botlist` | Get bot list |
| PUT | `/botlist` | Replace bot list |
| DELETE | `/botlist` | Clear bot list |
| POST | `/botlist/add` | Add IPs to bot list |
| POST | `/botlist/exclude` | Remove IPs from bot list |

---

## Facebook Integration

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/integrations/facebook` | List FB integrations |
| POST | `/integrations/facebook` | Create FB integration |
| GET | `/integrations/facebook/{id}` | Get FB integration |
| PUT | `/integrations/facebook/{id}` | Update FB integration |
| DELETE | `/integrations/facebook/{id}` | Delete FB integration |
| GET | `/integrations/facebook/{id}/campaign` | List assigned campaigns |
| POST | `/integrations/facebook/{id}/campaign` | Assign to campaign |
| DELETE | `/integrations/facebook/{id}/campaign` | Unassign from campaign |

---

## Click API (v3)

Separate from Admin API. Used to process clicks server-side (for custom integrations).

**Endpoint:** `GET/POST https://{tracker-domain}/click_api/v3`

### Request Parameters
- `token` (string, required) — campaign API token (from campaign settings)
- `ip` (string) — visitor IPv4 address
- `user_agent` (string) — visitor user agent
- `language` (string) — language ISO code
- `landing_id` (integer) — originating landing page ID
- `uniqueness_cookie` (string) — cookie data for visitor tracking
- `x_requested_with` (string) — browser header value
- `log` (integer) — set to 1 to include processing log
- `info` (integer) — set to 1 to include click info in response
- `force_redirect_offer` (integer) — set to 1 for offer redirect URL in body

### Response Fields
```json
{
  "headers": ["Location: https://offer.com/?sub=abc123"],
  "status": "302",
  "body": "",
  "contentType": "application/json; charset=utf-8",
  "uniqueness_cookie": "abc123def456",
  "cookies_ttl": 24,
  "log": ["Step 1: ...", "Step 2: ..."],
  "info": {
    "sub_id": "abc123",
    "campaign_id": 12,
    "stream_id": 45,
    "offer_id": [10],
    "token": "xyz789",
    "is_bot": false
  }
}
```

### Offer URL Construction
After getting `info.token` from Click API response:
```
https://{tracker-domain}/?_lp=1&_token={info.token}
```

### Status Codes
- 200 — success
- 401 — invalid token or campaign not found
- 409 — Click API feature disabled

---

## Postback & Conversion Tracking

### S2S Postback URL Format (incoming — from affiliate networks)
```
https://{tracker-domain}/postback?subid={subid}&payout={payout}&status={status}
```

### Postback Parameters
- `subid` (required) — unique click ID passed through landing to network
- `payout` (optional) — conversion payout amount
- `status` (optional) — conversion status: "lead", "sale", "rejected"
- `revenue` (optional) — alternative to payout

### Passing SubID Through Landing
Add hidden field in landing page forms:
```html
<input type="hidden" name="subid" value="{subid}">
```

Or pass via URL parameter:
```
https://offer.com/?aff_sub={subid}
```

### Keitaro LP Pixel (for local landings)
Include in landing page to track clicks and get subid:
```html
<script src="https://{tracker-domain}/landing.php?marker=1"></script>
```

### Supported Affiliate Networks (with templates)
Adcombo, Dr.Cash, HotPartners, KMA, Leadtrade, Leadvertex, LemonAD,
LuckyOnline, M1-Shop, M4Leads, Shakes.pro, TerraLeads, and 350+ more
via built-in templates.

### Macro Reference (for offer URLs)
- `{subid}` or `{sub_id}` — unique click identifier
- `{campaign_id}` — campaign ID
- `{stream_id}` — flow/stream ID
- `{creative_id}` — creative/ad ID (from traffic source)
- `{source}` — traffic source name
- `{keyword}` — keyword (from traffic source)
- `{country}` — visitor country code
- `{city}` — visitor city
- `{device}` — device type
- `{os}` — operating system
- `{browser}` — browser name
- `{ip}` — visitor IP
- `{user_agent}` — visitor user agent
- `{referrer}` — referrer URL
- `{sub_id_1}` through `{sub_id_15}` — custom sub-ID values

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (invalid params) |
| 401 | Unauthorized (invalid API key) |
| 402 | Payment required (license issue) |
| 404 | Not found |
| 406 | Not acceptable |
| 422 | Unprocessable entity (domain registration) |
| 500 | Server error |
