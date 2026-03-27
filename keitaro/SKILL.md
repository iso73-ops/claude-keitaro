---
name: keitaro
description: "Keitaro tracker management for affiliate marketers and media buyers. Manage campaigns, flows, landings, reports, and optimization via natural language through Keitaro Admin API. Supports all verticals: gambling, crypto, nutra, dating, finance, sweepstakes, e-commerce. Triggers on: keitaro, tracker, campaigns, flows, landings, TDS, traffic distribution, affiliate tracking, media buying, postback, conversion tracking, ROI optimization, split test."
argument-hint: "setup | campaigns | flows | reports | optimize | landing | audit"
license: MIT
---

# Keitaro — Tracker Management for Affiliate Marketers

Full Keitaro tracker control via natural language. Manage campaigns, flows,
landings, reports, and optimization through the Admin API.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/keitaro setup` | Connect to Keitaro API, verify access, save config |
| `/keitaro campaigns` | Create/list/update/delete campaigns |
| `/keitaro flows` | Manage traffic flows, weights, filters, A/B tests |
| `/keitaro reports` | Analytics: ROI, CR, EPC by campaign/flow/landing/geo/device |
| `/keitaro optimize` | Auto-optimize: kill losers, scale winners, rebalance weights |
| `/keitaro landing` | Generate landing/prelanding content for any vertical |
| `/keitaro audit` | Audit campaign setup: dead flows, broken postbacks, misconfig |

## Context Intake (Required — Always Do This First)

Before any operation, ensure Keitaro API connection is configured.
Check for `KEITARO_URL` and `KEITARO_API_KEY` environment variables.

If not set, run `/keitaro setup` first.

Ask these questions upfront if not already known:

1. **Vertical** — What are you running? Gambling, Crypto, Nutra, Dating, Finance,
   Sweepstakes, E-commerce, Health/Medical, Insurance, Software, Other
2. **GEOs** — Target countries
3. **Traffic source** — Where traffic comes from (Facebook, Google, TikTok, Push, Pop, Native, SEO)
4. **Goal** — What metric matters most? ROI, CR, EPC, Revenue, Volume

If the user provides context upfront (e.g. "create campaign for gambling DE"),
extract it and proceed without re-asking.

## API Connection

All API calls go through the Keitaro Admin API:

```
Base URL: {KEITARO_URL}/admin_api/v1
Headers: Api-Key: {KEITARO_API_KEY}
```

Use the `scripts/keitaro_api.py` helper for all API operations.
Run via: `python3 ~/.claude/skills/keitaro/scripts/keitaro_api.py <action> [args]`

## Orchestration Logic

When the user invokes `/keitaro`:

1. **Check API connection** — verify KEITARO_URL and KEITARO_API_KEY are set
2. **Parse command** — route to appropriate sub-skill
3. **Collect context** — vertical, GEO, traffic source if needed
4. **Execute** — call Keitaro API via helper script
5. **Report** — show results in clean, readable format

For `/keitaro audit`, spawn subagents in parallel:
- **campaign-analyzer** — analyze campaign performance across all campaigns
- **flow-optimizer** — check flow health, dead landings, weight distribution

## Reference Files

Load on-demand as needed — do NOT load all at startup.

**Path resolution:** All references are installed at `~/.claude/skills/keitaro/references/`.

- `references/keitaro-api.md` — Full Admin API reference (endpoints, methods, params)
- `references/verticals.md` — Vertical-specific benchmarks (CR, EPC, ROI targets by vertical+GEO)
- `references/optimization-rules.md` — Kill rules, scaling rules, weight distribution logic
- `references/landing-specs.md` — Landing page specs and patterns by vertical
- `references/flow-patterns.md` — Common flow patterns (white/offer, A/B, geo-split, device-split)

## Quality Gates

Hard rules — never violate these:

- Never delete a campaign without explicit user confirmation
- Never change flows on campaigns with active traffic without warning
- Kill Rule: flag any flow/landing with ROI < -30% over 100+ clicks for pause
- Scale Rule: flows with ROI > 30% over 200+ clicks are candidates for weight increase
- Always verify postback URL is configured before marking campaign as ready
- Never expose API key in outputs or logs
- Always show estimated impact before bulk operations ("this will affect X campaigns")

## Optimization Thresholds

Default thresholds (user can override):

| Metric | Kill | Warning | Good | Scale |
|--------|------|---------|------|-------|
| ROI | < -30% | -30% to 0% | 0% to 30% | > 30% |
| CR | < 0.5% | 0.5% to 1% | 1% to 3% | > 3% |
| EPC | < $0.05 | $0.05-0.15 | $0.15-0.50 | > $0.50 |
| Min clicks for decision | 100 | — | — | 200 |

These vary by vertical — load `references/verticals.md` for vertical-specific thresholds.

## Sub-Skills

This skill orchestrates 7 specialized sub-skills:

1. **keitaro-setup** — API connection and initial configuration
2. **keitaro-campaigns** — Campaign CRUD operations
3. **keitaro-flows** — Flow and traffic distribution management
4. **keitaro-reports** — Analytics and reporting
5. **keitaro-optimize** — Auto-optimization engine
6. **keitaro-landing** — Landing page generation and management
7. **keitaro-audit** — Campaign health audit

## Output Format

All reports follow this structure:

```markdown
## [Report Title]
**Period:** [date range]
**Campaigns analyzed:** [count]

### Summary
[Key findings in 2-3 bullets]

### Details
[Tables with metrics]

### Actions
- [Prioritized action items with expected impact]
```
