# Common Flow Patterns in Keitaro

## Pattern 1: White Page + Offer (Cloaking)

Standard setup for traffic sources with strict moderation (Facebook, Google, TikTok).

```
Campaign
├── Flow 1: "White" (default/safe page)
│   ├── Type: default
│   ├── Filters: none (catches everything that doesn't match other flows)
│   ├── Schema: landings
│   └── Landing: safe/compliant white page
│
├── Flow 2: "Offer — Desktop"
│   ├── Type: regular
│   ├── Weight: 100
│   ├── Filters:
│   │   ├── geo: accept [target GEOs]
│   │   ├── device_type: accept [desktop]
│   │   └── referrer: accept [traffic source domain]
│   ├── Schema: landings → offers
│   ├── Landings: [prelanding_1, prelanding_2]
│   └── Offers: [offer_1]
│
└── Flow 3: "Offer — Mobile"
    ├── Type: regular
    ├── Weight: 100
    ├── Filters:
    │   ├── geo: accept [target GEOs]
    │   ├── device_type: accept [mobile, tablet]
    │   └── referrer: accept [traffic source domain]
    ├── Schema: landings → offers
    ├── Landings: [mobile_prelanding_1]
    └── Offers: [offer_1_mobile]
```

**When to use:** Facebook, Google, TikTok campaigns where moderation bots must see a clean page.

**Key principle:** Default flow (white) catches bots, moderators, and non-target traffic. Regular flows with filters catch real target users.

---

## Pattern 2: A/B Test Landings

Testing multiple landings within a single flow or across flows.

### Option A: Same Flow, Multiple Landings
```
Campaign
└── Flow 1: "Main"
    ├── Weight: 100
    ├── Schema: landings → offers
    ├── Landings:
    │   ├── landing_A (weight: 50)
    │   └── landing_B (weight: 50)
    └── Offers: [offer_1]
```

### Option B: Separate Flows per Landing
```
Campaign
├── Flow 1: "Test A"
│   ├── Weight: 50
│   ├── Schema: landings → offers
│   ├── Landings: [landing_A]
│   └── Offers: [offer_1]
│
└── Flow 2: "Test B"
    ├── Weight: 50
    ├── Schema: landings → offers
    ├── Landings: [landing_B]
    └── Offers: [offer_1]
```

**Option A** is simpler. **Option B** gives better per-flow reporting in Keitaro.

---

## Pattern 3: GEO Split

Different offers/landings per country.

```
Campaign (multi-GEO)
├── Flow 1: "Germany"
│   ├── Filters: geo: accept [DE]
│   ├── Landings: [landing_de]
│   └── Offers: [offer_de]
│
├── Flow 2: "Austria"
│   ├── Filters: geo: accept [AT]
│   ├── Landings: [landing_at]
│   └── Offers: [offer_at]
│
├── Flow 3: "Switzerland"
│   ├── Filters: geo: accept [CH]
│   ├── Landings: [landing_ch]
│   └── Offers: [offer_ch]
│
└── Flow 4: "Default — Block"
    ├── Type: default
    └── Action: show 404 / redirect to white page
```

**When to use:** Same traffic source campaign targets multiple GEOs (common with push/pop/native).

---

## Pattern 4: Device/OS Split

```
Campaign
├── Flow 1: "iOS"
│   ├── Filters: os: accept [iOS]
│   ├── Landings: [ios_landing]
│   └── Offers: [ios_offer]
│
├── Flow 2: "Android"
│   ├── Filters: os: accept [Android]
│   ├── Landings: [android_landing]
│   └── Offers: [android_offer]
│
└── Flow 3: "Desktop"
    ├── Filters: device_type: accept [desktop]
    ├── Landings: [desktop_landing]
    └── Offers: [desktop_offer]
```

**When to use:** App offers, software downloads, mobile-specific offers.

---

## Pattern 5: Offer Rotation

Testing multiple offers with same landing.

```
Campaign
└── Flow 1: "Main"
    ├── Schema: landings_offers
    ├── Landings: [prelanding_1]
    └── Offers:
        ├── offer_A (weight: 40) — Network 1
        ├── offer_B (weight: 40) — Network 2
        └── offer_C (weight: 20) — Network 3 (testing)
```

**When to use:** Same product/vertical available on multiple networks. Compare payouts, approve rates, hold times.

---

## Pattern 6: Funnel (Prelanding → Landing → Offer)

Multi-step funnel with prelanding warmup.

```
Campaign
└── Flow 1: "Funnel"
    ├── Schema: landings → offers
    ├── Landings:
    │   └── prelanding (advertorial/quiz)
    │       └── onClick → landing (product page/registration)
    └── Offers: [offer_1]
```

**How it works in Keitaro:**
1. User hits campaign URL → sees prelanding
2. Prelanding CTA links to `{offer_url}` or next step via LP pixel
3. User reaches offer page via Keitaro redirect

---

## Pattern 7: Time-Based Rotation

Different flows by time of day.

```
Campaign
├── Flow 1: "Daytime (08-20)"
│   ├── Filters: hour: accept [8,9,10,11,12,13,14,15,16,17,18,19,20]
│   ├── Landings: [daytime_landing]
│   └── Offers: [daytime_offer]
│
└── Flow 2: "Nighttime (20-08)"
    ├── Filters: hour: accept [21,22,23,0,1,2,3,4,5,6,7]
    ├── Landings: [night_landing]
    └── Offers: [night_offer]
```

**When to use:** Gambling (night performs better), B2B (business hours only), dating (evening/night).

---

## Pattern 8: Sub-ID Routing

Route traffic by source sub-ID (e.g., different creatives or ad sets).

```
Campaign
├── Flow 1: "Creative A traffic"
│   ├── Filters: sub_id_2: accept [creative_a_id]
│   ├── Landings: [landing_matching_creative_a]
│   └── Offers: [offer_1]
│
└── Flow 2: "Creative B traffic"
    ├── Filters: sub_id_2: accept [creative_b_id]
    ├── Landings: [landing_matching_creative_b]
    └── Offers: [offer_1]
```

**When to use:** Message match between ad creative and landing page. Different messaging for different audiences.

---

## Quick Reference: Schema Types

| Schema | Flow Structure | Use Case |
|--------|---------------|----------|
| `redirect` | Direct redirect to URL | Simple redirect to offer |
| `landings` | Show landing page | Landing only, no offer |
| `offers` | Redirect to offer | Direct linking |
| `landings_offers` | Landing → Offer | Full funnel with prelanding |

## Quick Reference: Stream Types

| Type | Behavior |
|------|----------|
| `regular` | Normal flow, filtered by conditions + weight |
| `forced` | Evaluated FIRST, top to bottom, bypasses regular rotation. Used for specific sub-ids or priority routing |
| `default` | Fallback — catches all traffic that doesn't match regular/forced flows. If missing → "Do Nothing" |

## Quick Reference: Campaign Rotation Modes

| Mode | `type` value | Behavior |
|------|-------------|----------|
| Position-based | `"position"` | Flows evaluated sequentially top to bottom. First matching flow wins |
| Weight-based | `"weight"` | Flows selected randomly based on weight %. Needs large sample for accuracy (law of large numbers) |

## Quick Reference: Visitor Binding (weight-based only)

| Binding | `bind_visitors` value | What's preserved |
|---------|----------------------|------------------|
| Flow only | `"flow"` | Returning visitor goes to same flow |
| Flow + Landing | `"flow_landing"` | Same flow and same landing page |
| Flow + Landing + Offer | `"flow_landing_offer"` | Same flow, landing, and offer |

Binding TTL: 1-8760 hours (default 24). Set via `bind_visitors_ttl`.

## Quick Reference: Favorite Flows

Flows marked as favorites become reusable templates. Inserting a favorite into another campaign creates a **clone** (not a shared reference). Useful for standardizing cloaking setups across campaigns.

## Import/Export

Flows can be exported/imported as JSON files for portability between trackers.
