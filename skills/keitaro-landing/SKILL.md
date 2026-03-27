---
name: keitaro-landing
description: >
  Generate landing page and prelanding content for any affiliate vertical.
  Create, list, update, and manage landing pages in Keitaro. Use when user says
  "generate landing", "create landing", "prelanding", "new landing page",
  "white page", or describes landing page needs.
---

# Keitaro Landing Page Management

## Process

1. Read `keitaro/references/landing-specs.md` for vertical-specific specs
2. Read `keitaro/references/keitaro-api.md` for landing API endpoints
3. Determine landing type (prelanding, landing, white page)
4. Generate content or manage existing landings
5. Create/update in Keitaro via API

## Landing Types

### Prelanding (Advertorial/Quiz)
Warmup page before offer. Increases CR by qualifying traffic.
- Advertorial (fake news article)
- Quiz/survey funnel
- Review/comparison page
- Success story

### Landing (Product/Registration Page)
Main conversion page.
- Product page
- Registration form
- Bonus/offer page

### White Page (Safe/Compliant)
Clean page for moderation bots.
- Blog article (health, travel, cooking)
- Company page
- News article
- Must pass Facebook/Google moderation

## Generate Landing Content

When user says "generate a prelanding for [vertical] [GEO]":

1. Identify vertical from `references/landing-specs.md`
2. Determine language from GEO
3. Generate content following vertical specs:
   - Headline (hook)
   - Body (story/review/quiz)
   - CTA button text
   - Trust elements
   - Required disclaimers
4. Output as HTML

### Content Generation Guidelines

- Write in target GEO language (or English if user prefers)
- Follow vertical-specific structure from `references/landing-specs.md`
- Include all required compliance elements
- Mobile-first design
- Fast-loading (minimal external resources)

## List Landings

```bash
python3 ~/.claude/skills/keitaro/scripts/keitaro_api.py landings list
```

Show as table:
```
| ID | Name | Type | Group | Offers | Updated |
|----|------|------|-------|--------|---------|
| 5  | gambling_de_v1 | redirect | Gambling | offer_1 | 2d ago |
| 6  | gambling_de_v2 | redirect | Gambling | offer_1 | 1d ago |
| 8  | white_blog | local | White | — | 5d ago |
```

## Create Landing in Keitaro

After generating content:

1. Create landing via API:
```json
{
  "name": "gambling_de_prelanding_v1",
  "action_type": "redirect",
  "url": "https://example.com/prelanding/",
  "group_id": 1
}
```

For local landings (HTML):
```json
{
  "name": "white_page_cooking_blog",
  "action_type": "html",
  "action_payload": "<html>...</html>"
}
```

2. Assign to campaign flow if requested

## White Page Generator

When user says "generate white page":

1. Pick a safe niche (cooking, travel, wellness, technology)
2. Generate a legitimate-looking blog article
3. Include:
   - Realistic header/nav
   - Article content (500-800 words)
   - Stock photo placeholders
   - Footer with links
4. No affiliate links, no suspicious CTAs
5. Must look like a real blog/news site
