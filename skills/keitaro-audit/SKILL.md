---
name: keitaro-audit
description: >
  Audit Keitaro campaign health: dead flows, broken postbacks, misconfigured
  filters, missing white pages, domain issues. Use when user says "audit",
  "health check", "what's broken", "check my campaigns", or "find problems".
---

# Keitaro Campaign Audit

## Process

1. Read `keitaro/references/keitaro-api.md` for API endpoints
2. Read `keitaro/references/flow-patterns.md` for expected patterns
3. Read `keitaro/references/optimization-rules.md` for thresholds
4. Pull all campaign and flow data
5. Run audit checks
6. Generate health report with findings

## Audit Checks (35 total)

### Campaign Health (10 checks)

| ID | Check | Severity |
|----|-------|----------|
| C01 | Campaign has at least 1 active flow | Critical |
| C02 | Campaign has a default flow (white page) | High |
| C03 | Campaign is linked to a traffic source | Medium |
| C04 | Campaign has a domain assigned | High |
| C05 | Campaign alias is set and valid | Medium |
| C06 | Campaign cost model is configured | Medium |
| C07 | Campaign has no empty/orphan flows | Low |
| C08 | Campaign name follows naming convention | Low |
| C09 | Campaign has conversions in last 7 days | Warning |
| C10 | Campaign is not spending with 0 conversions for 48h+ | Critical |

### Flow Health (10 checks)

| ID | Check | Severity |
|----|-------|----------|
| F01 | Flow has at least 1 landing or offer assigned | Critical |
| F02 | Flow filters are not contradictory | High |
| F03 | Flow GEO filter matches campaign intent | Medium |
| F04 | Flow weight is > 0 for active flows | Medium |
| F05 | Flow schema matches landing/offer setup | High |
| F06 | Total flow weights don't exceed 100 logical distribution | Low |
| F07 | No duplicate flows (same filters + same landings) | Low |
| F08 | Default flow exists and has a safe landing | High |
| F09 | Flow is receiving traffic (clicks > 0 in 48h) | Warning |
| F10 | Flow ROI is not critically negative (< -50%) | Critical |

### Postback & Tracking (8 checks)

| ID | Check | Severity |
|----|-------|----------|
| T01 | Affiliate network has postback URL configured | Critical |
| T02 | Postback URL contains required macros ({subid}, etc.) | Critical |
| T03 | Conversions received in last 7 days | High |
| T04 | Conversion count matches approximate offer network stats | Medium |
| T05 | Traffic source postback configured (for auto-cost) | Medium |
| T06 | Click-to-conversion time is reasonable (not instant) | Medium |
| T07 | No duplicate conversions detected | High |
| T08 | S2S postback preferred over pixel (reliability) | Low |

### Domain Health (4 checks)

| ID | Check | Severity |
|----|-------|----------|
| D01 | Domain DNS resolves correctly | Critical |
| D02 | Domain SSL certificate valid | High |
| D03 | Domain is not flagged/blocked by traffic source | Critical |
| D04 | Domain age > 7 days for paid traffic | Medium |

### Landing Health (3 checks)

| ID | Check | Severity |
|----|-------|----------|
| L01 | Landing URL is accessible (HTTP 200) | Critical |
| L02 | Landing loads in < 5 seconds | High |
| L03 | Landing has tracking pixel/script installed | High |

## Scoring

### Campaign Health Score (0-100)

```
Score = 100 - Sum(failed_checks × severity_weight)
```

Severity weights:
- Critical: 15 points
- High: 8 points
- Medium: 4 points
- Low: 2 points
- Warning: 1 point (informational)

### Grading

| Grade | Score | Status |
|-------|-------|--------|
| A | 90-100 | Healthy |
| B | 75-89 | Minor issues |
| C | 60-74 | Needs attention |
| D | 40-59 | Significant problems |
| F | < 40 | Urgent fixes needed |

## Output Format

```
Keitaro Audit Report
════════════════════
Date: Mar 27, 2026
Campaigns analyzed: 8
Overall Health Score: 73/100 (C)

CRITICAL (fix immediately):
  ✗ [C10] Campaign #21 "dating_us" spending $45/day with 0 conversions for 3 days
  ✗ [T01] Campaign #25 "crypto_ch" — affiliate network missing postback URL
  ✗ [F01] Campaign #12 Flow "Test C" has no landing or offer assigned

HIGH (fix within 24h):
  ⚠ [C02] Campaign #18 "nutra_br" has no default/white flow
  ⚠ [D02] Domain tracker3.example.com SSL expires in 5 days

MEDIUM (fix within 7 days):
  ○ [C06] Campaign #15 has no cost model set (ROI calculation inaccurate)
  ○ [F03] Campaign #12 Flow "DE" has GEO filter for DE,AT but campaign name says DE only

Quick Wins:
  1. Add postback to campaign #25 (2 min fix, blocks revenue tracking)
  2. Pause campaign #21 (saves $45/day until fixed)
  3. Assign landing to Flow "Test C" in campaign #12
```

## Parallel Execution

For full audit, spawn subagents:
- **campaign-analyzer** — checks C01-C10, pulls reports
- **flow-optimizer** — checks F01-F10, analyzes flow structure

Collect results and merge into unified report.
