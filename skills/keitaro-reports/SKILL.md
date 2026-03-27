---
name: keitaro-reports
description: >
  Build and display Keitaro analytics reports. Campaign, flow, landing, offer,
  GEO, device breakdowns with ROI/CR/EPC metrics. Use when user says "report",
  "stats", "analytics", "show me", "what's performing", "what's losing money",
  "ROI", or asks about performance data.
---

# Keitaro Reports & Analytics

## Process

1. Read `keitaro/references/keitaro-api.md` for report endpoint
2. Read `keitaro/references/verticals.md` for vertical-specific benchmarks
3. Parse what user wants to see (grouping, metrics, date range, filters)
4. Build report via `POST /report/build`
5. Format and display with color-coded health indicators

## Report Builder

### Default Report (when user just says "show stats")

```json
{
  "range": {"from": "<7 days ago>", "to": "<today>", "timezone": "UTC"},
  "metrics": ["clicks", "campaign_unique_clicks", "conversions", "revenue", "cost", "profit", "roi", "cr", "epc"],
  "grouping": ["campaign_id"],
  "sort": [{"name": "cost", "order": "desc"}],
  "summary": true,
  "limit": 50
}
```

### Common Report Types

**"What's performing?"** → Top campaigns by ROI (ROI > 0, sorted desc)
**"What's losing money?"** → Campaigns with negative profit, sorted by loss
**"Show me campaign 12 by GEO"** → Campaign filter + country grouping
**"Landing performance for campaign 12"** → Campaign filter + landing_page_id grouping
**"Hourly breakdown today"** → Today range + hour grouping
**"Compare this week vs last week"** → Two report calls, side by side

## Output Format

### Campaign Overview
```
Campaign Performance (Mar 20-27, 2026)
──────────────────────────────────────────────────────────────────
ID  | Name           | Clicks | Conv | Revenue | Cost   | Profit  | ROI    | CR
12  | gambling_de     | 5,432  | 89   | $4,450  | $2,716 | $1,734  | +63%   | 1.6%
15  | crypto_at       | 1,203  | 12   | $2,400  | $1,804 | $596    | +33%   | 1.0%
18  | nutra_br        | 890    | 45   | $675    | $445   | $230    | +52%   | 5.1%
21  | dating_us       | 3,210  | 28   | $140    | $321   | -$181   | -56%   | 0.9%
──────────────────────────────────────────────────────────────────
Total                 | 10,735 | 174  | $7,665  | $5,286 | $2,379  | +45%   | 1.6%
```

### Flow Breakdown
```
Campaign #12: gambling_de — Flow Breakdown
──────────────────────────────────────────────────
Flow    | Weight | Clicks | Conv | CR   | ROI
DE Mob  | 60%    | 3,259  | 62   | 1.9% | +78%
DE Desk | 30%    | 1,629  | 22   | 1.4% | +41%
Test    | 10%    | 544    | 5    | 0.9% | -12%
```

## Health Indicators

Apply thresholds from `references/verticals.md`:

- **ROI > scale threshold**: mark as SCALE candidate
- **ROI in good range**: mark as STABLE
- **ROI in warning range**: mark as WARNING
- **ROI < kill threshold**: mark as KILL candidate
- **Insufficient data** (clicks < min threshold): mark as TESTING

## Smart Insights

After showing the report, add 2-3 actionable insights:

1. **Best performer:** "Campaign #12 is your best. ROI +63%, consider scaling budget +20%"
2. **Worst performer:** "Campaign #21 is bleeding $181. ROI -56% on 3.2k clicks. Kill or restructure"
3. **Test update:** "Flow 'Test' in campaign #12 needs 56 more clicks before we can decide"

## Date Range Shortcuts

Parse natural language date ranges:
- "today" → today
- "yesterday" → yesterday
- "last 7 days" / "this week" → 7 day range
- "last 30 days" / "this month" → 30 day range
- "last 3 days" → 3 day range
- "March" → full month
- Specific dates: "Mar 15 to Mar 20"

Default to **last 7 days** if not specified.
