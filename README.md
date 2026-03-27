<p align="center">
  <img src="assets/banner.png" alt="Claude Keitaro — Keitaro Tracker Skill for Claude Code" width="100%">
</p>

# Claude Keitaro — Keitaro Tracker Management for Claude Code

Manage your Keitaro tracker with natural language. Create campaigns, optimize flows, generate landings, analyze performance — all through Claude Code. Built for affiliate marketers and media buyers.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What It Does

Talk to your Keitaro tracker like a human:

```
You: create campaign for gambling, GEO Germany, 3 landings
Claude: Created campaign "gambling_de_20260327" with 3 flows...

You: what's losing money?
Claude: Campaign #21 "dating_us" — ROI -56%, burning $45/day. Kill it?

You: optimize all campaigns
Claude: Found 5 flows to kill (saving $85/day), 3 to scale (+$45/day). Apply?

You: setup cloaking for campaign 12
Claude: Created default flow (white page) + offer flow with GEO/referrer filters. Done.
```

## Installation

### One-Command Install (macOS/Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/iso73-ops/claude-keitaro/main/install.sh | bash
```

### One-Command Install (Windows PowerShell)

```powershell
irm https://raw.githubusercontent.com/iso73-ops/claude-keitaro/main/install.ps1 | iex
```

### Manual Install

```bash
git clone https://github.com/iso73-ops/claude-keitaro.git
cd claude-keitaro
./install.sh
```

## Setup

1. Set environment variables:

```bash
export KEITARO_URL="https://your-tracker.com"
export KEITARO_API_KEY="your-api-key"
```

2. Start Claude Code and verify:

```bash
claude
/keitaro setup
```

## Commands

| Command | Description |
|---------|-------------|
| `/keitaro setup` | Connect to Keitaro API, verify access, show tracker status |
| `/keitaro campaigns` | Create, list, update, disable, enable, clone, delete campaigns |
| `/keitaro flows` | Manage flows, weights, filters, A/B tests, cloaking patterns |
| `/keitaro reports` | Analytics by campaign, flow, landing, offer, GEO, device, time |
| `/keitaro optimize` | Auto-optimize: kill losers, scale winners, rebalance weights |
| `/keitaro landing` | Generate landing/prelanding/white page content for any vertical |
| `/keitaro audit` | Health check: 35 checks across campaigns, flows, postbacks, domains |

## Supported Verticals

All verticals with built-in benchmarks (ROI/CR/EPC thresholds, typical payouts, top GEOs):

| Vertical | Key Metrics | Typical Payouts |
|----------|-------------|-----------------|
| Gambling / Casino / Betting | FTD, CPA per FTD | $50-200 CPA, 25-45% RevShare |
| Crypto / Trading / Forex | CPL, FTD deposit | $200-1000 CPA |
| Nutra / Health & Beauty | Sale CR, approve rate | $15-80 CPA (COD/SS) |
| Dating / Adult | SOI/DOI reg rate | $2-60 per action |
| Finance / Loans / Insurance | CPL, approval rate | $10-300 CPL |
| Sweepstakes / Leadgen | SOI/DOI/CC submit | $0.50-25 per action |
| E-commerce / Dropshipping | ROAS, AOV, purchase CR | Varies |
| Medical / Health Clinics | CPL, lead quality | $50-500 per lead |
| Software / Apps / Utilities | Install rate, trial-to-paid | $0.50-80 per action |

## Features

### Direct API Integration
Unlike tools that work with exports and screenshots, Claude Keitaro connects **directly to your tracker** via the Admin API. Supports Admin API v1 + Click API v3.

**Full CRUD operations:**
- Campaigns (create, list, get, update, disable, enable, clone, delete, costs)
- Streams/Flows (create, update, disable, enable, clone, restore)
- Landing Pages (create, list, update, clone, upload files, download)
- Offers (create, list, update, clone, with payout config)
- Domains (list, check DNS/SSL status, register via Namecheap)
- Affiliate Networks, Traffic Sources, Groups
- Reports, Click Log, Conversion Log
- Bot List management
- Facebook Integration

### 35 Audit Checks

| Category | Checks | Key Areas |
|----------|--------|-----------|
| Campaign Health | 10 | Active flows, default flow, traffic source, domain, costs |
| Flow Health | 10 | Landing/offer assigned, filter logic, weights, traffic |
| Postback & Tracking | 8 | Postback URL, macros, conversion matching, S2S vs pixel |
| Domain Health | 4 | DNS, SSL, blocking, age |
| Landing Health | 3 | Accessibility, load time, tracking pixel |

Weighted scoring (Critical 15pts, High 8pts, Medium 4pts, Low 2pts) with letter grades A-F.

### Smart Optimization

- **Kill rules**: auto-detect flows with ROI below vertical threshold (e.g., < -30% on 100+ clicks)
- **Scale rules**: identify flows with strong ROI for weight increase
- **Minimum sample sizes**: prevents premature decisions (100-400 clicks depending on vertical)
- **A/B test logic**: 95% confidence before declaring winner
- **Day-parting awareness**: doesn't kill campaigns based on 1 bad day

### Flow Pattern Library

Pre-built patterns ready to deploy:

| Pattern | Use Case |
|---------|----------|
| White + Offer (Cloaking) | Facebook, Google, TikTok campaigns |
| A/B Test Landings | Testing multiple landings with equal/weighted split |
| GEO Split | Different offers/landings per country |
| Device/OS Split | iOS vs Android vs Desktop routing |
| Offer Rotation | Testing multiple networks/payouts |
| Time-Based Routing | Day-parting by vertical (gambling: night, B2B: business hours) |
| Sub-ID Routing | Message match between ad creative and landing |
| Funnel (Pre > Land > Offer) | Multi-step warmup flow |

### Landing Generator

Generate content in **any language** for any vertical:
- **Prelandings**: advertorials, quiz funnels, review pages, success stories
- **Landings**: product pages, registration forms, bonus pages
- **White pages**: safe blog articles for moderation (cooking, travel, tech)

Follows vertical-specific templates with required compliance elements.

## Safety System

4 levels of protection to prevent breaking live traffic:

| Level | What It Does | How It Works |
|-------|-------------|-------------|
| **Dry Run** | Preview without executing | `--dry-run` flag blocks all writes, shows payload |
| **Auto Snapshots** | Save state before changes | JSON backup to `~/.claude/keitaro-snapshots/` |
| **Traffic Detection** | Warn about live campaigns | Checks last 24h clicks/cost before modification |
| **Last-Flow Guard** | Block killing all traffic | Prevents disabling the only active flow (requires `--force`) |

```bash
# Always safe — see what would happen without doing it
python3 keitaro_api.py --dry-run campaign disable --id 12

# Output:
# [DRY RUN] Would execute: POST /campaigns/12/disable
# [SAFETY] WARNING: Campaign #12 has LIVE TRAFFIC!
# [SAFETY]   Last 24h: 5,432 clicks, $271.60 spent
```

## Architecture

```
~/.claude/skills/keitaro/              # Main orchestrator + references + API helper
~/.claude/skills/keitaro/references/   # 5 reference files
    keitaro-api.md                     #   Full Admin API + Click API v3 reference
    verticals.md                       #   Benchmarks by vertical (9 verticals)
    optimization-rules.md              #   Kill/scale/A/B test decision logic
    landing-specs.md                   #   Landing templates by vertical
    flow-patterns.md                   #   8 flow patterns with examples
~/.claude/skills/keitaro/scripts/
    keitaro_api.py                     #   Python API helper (548 lines)
~/.claude/skills/keitaro-*/            # 7 sub-skills
    keitaro-setup/                     #   API connection & verification
    keitaro-campaigns/                 #   Campaign CRUD
    keitaro-flows/                     #   Flow/stream management
    keitaro-reports/                   #   Analytics & reporting
    keitaro-optimize/                  #   Auto-optimization engine
    keitaro-landing/                   #   Landing page generation
    keitaro-audit/                     #   35-check health audit
~/.claude/agents/                      # 3 subagents
    campaign-analyzer.md               #   Campaign performance analysis
    flow-optimizer.md                  #   Flow health & optimization
    landing-generator.md               #   Landing content generation
```

### How It Works

1. **Orchestrator** (`/keitaro`) routes commands to specialized sub-skills
2. **Sub-skills** handle specific domains (campaigns, flows, reports, etc.)
3. **Agents** run in parallel for audits and bulk analysis
4. **References** load on-demand (RAG pattern) — only what's needed per operation
5. **API helper** (`keitaro_api.py`) handles all Keitaro API calls with built-in safety
6. **Snapshots** auto-saved before any destructive operation

## API Helper CLI

The Python helper can also be used standalone:

```bash
# Test connection
python3 keitaro_api.py test

# List campaigns
python3 keitaro_api.py campaigns

# Create campaign
python3 keitaro_api.py campaign create --name "gambling_de" --alias "gamb-de-1" \
  --type weight --cost-type CPC --cost-value 0.05

# Get campaign flows
python3 keitaro_api.py streams --campaign-id 12

# Build report
python3 keitaro_api.py report --grouping campaign_id --range 7d \
  --metrics clicks,conversions,revenue,cost,profit,roi,cr,epc

# Dry run (safe preview)
python3 keitaro_api.py --dry-run stream disable --id 45
```

## Requirements

- Claude Code CLI
- Python 3.10+ with `requests` package
- Keitaro tracker with Admin API access (API key from Account > API keys)

## Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/iso73-ops/claude-keitaro/main/uninstall.sh | bash
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built for Claude Code by [@iso73-ops](https://github.com/iso73-ops)
