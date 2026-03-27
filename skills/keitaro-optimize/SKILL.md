---
name: keitaro-optimize
description: >
  Auto-optimize Keitaro campaigns: kill losing flows, scale winners, rebalance
  weights, suggest actions. Use when user says "optimize", "auto-optimize",
  "kill losers", "scale winners", "rebalance", "what should I pause", or
  "what should I scale".
---

# Keitaro Auto-Optimization

## Process

1. Read `keitaro/references/optimization-rules.md` for decision logic
2. Read `keitaro/references/verticals.md` for vertical-specific thresholds
3. Pull performance data via report API
4. Apply rules to identify actions
5. Present action plan with estimated impact
6. Execute only after user confirmation

## Optimization Pipeline

### Step 1: Collect Data
Build report grouped by `stream_id` with metrics:
clicks, conversions, revenue, cost, profit, roi, cr, epc

### Step 2: Classify Each Flow

For each flow, determine status based on vertical thresholds:

| Status | Condition | Action |
|--------|-----------|--------|
| KILL | ROI < kill threshold AND clicks >= min | Recommend pause |
| WARNING | ROI in warning range | Monitor, flag |
| STABLE | ROI in good range | Keep running |
| SCALE | ROI > scale threshold AND clicks >= scale min | Recommend weight increase |
| TESTING | clicks < min threshold | Wait for data |

### Step 3: Generate Action Plan

Present as prioritized list:

```
Optimization Plan — Campaign #12
═══════════════════════════════════════

KILL (save $X/day):
  ✗ Flow "Test Landing C" — ROI: -45%, 180 clicks, 0 conv
    → Action: Pause flow (saves ~$15/day)

SCALE (earn +$X/day):
  ↑ Flow "DE Mobile" — ROI: +78%, 3,259 clicks, 62 conv
    → Action: Increase weight 60% → 70% (est. +$12/day)

TESTING (wait):
  ? Flow "New Offer X" — ROI: +15%, 45 clicks, 2 conv
    → Action: Need 55 more clicks before decision

TOTAL ESTIMATED IMPACT: +$27/day
```

### Step 4: Execute (After Confirmation)

Only execute after user says "yes", "do it", "apply", etc.

Actions:
- Kill → `POST /streams/{id}/disable`
- Scale → `PUT /streams/{id}` with new weight
- Rebalance → adjust all weights proportionally

## Bulk Optimization

When user says "optimize all campaigns":

1. Get all active campaigns
2. Build report grouped by campaign_id
3. For each campaign with sufficient data:
   - Run flow-level optimization
   - Aggregate actions
4. Present summary:

```
Bulk Optimization Summary
═════════════════════════
Campaigns analyzed: 8
Flows to kill: 5 (saving ~$85/day)
Flows to scale: 3 (est. +$45/day)
Flows still testing: 12

Net estimated impact: +$130/day
```

## Safety Rules

- **ALWAYS run with `--dry-run` first** — show plan to user, get confirmation, then execute
- **Never auto-execute without explicit user confirmation** ("yes", "do it", "apply")
- Never kill all flows in a campaign (API helper blocks this automatically)
- Never set a single flow above 80% weight
- Don't optimize campaigns with < 24h of data
- Don't optimize during known traffic spikes (user must confirm)
- Show "undo" instructions after every action
- **Snapshots are automatic** — every stream/campaign is saved before modification
- For bulk operations: execute one at a time, verify result before next
- If ANY API call fails during bulk optimization: STOP immediately, report what was done

## Undo Instructions

After each optimization action, show how to reverse:

```
Applied: Paused flow #45 in campaign #12
Undo: Run `/keitaro flows` → "enable flow 45 in campaign 12"
```
