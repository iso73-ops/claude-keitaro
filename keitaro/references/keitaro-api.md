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
- `alias` (string, required) — URL alias
- `state` (string) — "active", "disabled"
- `cost_type` (string) — "CPC", "CPM", "CPA", "RevShare", "CPS"
- `cost_value` (number) — cost amount
- `cost_currency` (string) — "USD", "EUR", etc.
- `cost_auto` (boolean) — auto-pull costs from traffic source
- `group_id` (integer) — group for organization
- `bind_visitors` (string) — visitor binding mode
- `traffic_source_id` (integer) — linked traffic source
- `domain_id` (integer) — tracker domain to use
- `parameters` (object) — custom sub-id parameters mapping

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
- `sub_id_*` — sub-id values (sub_id_1 through sub_id_15)

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
| 500 | Server error |
