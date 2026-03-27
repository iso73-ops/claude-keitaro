# Optimization Rules & Decision Logic

## Kill Rules (When to Pause)

### Flow-Level Kill
Pause a flow when ALL conditions met:
1. Clicks >= min threshold for vertical (default: 100)
2. ROI < kill threshold for vertical (default: -30%)
3. No conversions in last 24h (if previously converting)

### Landing-Level Kill
Pause a landing within a flow when:
1. Clicks >= 50 on this specific landing
2. CR is 50%+ below the campaign average CR
3. At least one other landing in the same flow has 2x better CR

### Offer-Level Kill
Switch offer when:
1. Approve rate drops below 30% (nutra COD)
2. EPC drops 50%+ vs. 7-day average
3. Hold time exceeds 30 days with no movement

---

## Scale Rules (When to Increase)

### Weight Increase
Increase flow weight when ALL conditions met:
1. Clicks >= scale threshold for vertical (default: 200)
2. ROI > scale threshold for vertical (default: 30%)
3. Stable or improving trend over last 3 days
4. CR is above campaign average

### Scale Increments
- Current weight < 30%: increase by 10 points
- Current weight 30-60%: increase by 5 points
- Current weight > 60%: increase by 2-3 points (careful, already dominant)
- Never set any single flow above 80% weight (keep diversification)

### Campaign Budget Scale
Recommend budget increase when:
1. Campaign ROI > 20% sustained over 7 days
2. CR is stable (not declining)
3. Budget is fully spent daily
4. Scale by max 20-30% per increase (avoid learning phase reset)

---

## A/B Test Rules

### Minimum Sample Size
- For CR comparison: min 100 clicks per variant
- For ROI comparison: min 200 clicks per variant
- For revenue comparison: min 50 conversions per variant

### Statistical Confidence
- Use 95% confidence before declaring a winner
- Quick rule: if one variant has 2x CR with 100+ clicks each, it's likely winner
- If results are within 20% of each other after 200+ clicks, keep running

### Test Priority
1. Landing pages first (biggest impact on CR)
2. Offers second (impact on EPC/payout)
3. Flow filters third (GEO, device, OS targeting)
4. Prelandings last (if applicable)

---

## Weight Distribution Patterns

### Equal Split (testing phase)
All flows at equal weight. Use when:
- Starting new campaign
- Testing new landings/offers
- No data yet

### Winner-Takes-More (optimization phase)
Best performer gets highest weight, others get lower. Use when:
- Have 200+ clicks per flow
- Clear performance differences exist
- Want to maximize profit while still testing

### Suggested Distribution After Testing
```
Top performer:     50-60% weight
Second best:       20-30% weight
Testing slot:      10-20% weight (for new landings/offers)
```

### Rotation Strategies
- **Weighted random** (default): distribute by weight percentage
- **Priority**: send all traffic to top flow, fallback to next if filtered
- **Time-based**: rotate by hour/day (for freshness)

---

## Automated Actions

### Auto-Pause Triggers
1. Flow ROI < -50% after 200+ clicks → immediate pause
2. Landing CR = 0% after 100+ clicks → pause landing
3. Postback not received for 48h on active campaign → alert (don't pause)
4. Bot rate > 30% on a flow → alert + check filters

### Auto-Scale Triggers
1. Flow ROI > 50% after 300+ clicks, stable 3 days → increase weight +10
2. Campaign at budget cap with ROI > 30% → recommend budget increase

### Alert Triggers (Don't Auto-Act, Just Notify)
1. CR dropped 50%+ vs. yesterday → "CR drop alert"
2. Cost increased but no conversions in 6h → "spend without conversions"
3. New flow getting 0 clicks → "flow not receiving traffic"
4. Domain health check failed → "domain down"

---

## Time-Based Considerations

### Day-Parting
- Gambling: peak 18:00-02:00 local time
- Dating: peak 20:00-01:00 local time
- E-commerce: peak 10:00-14:00 and 19:00-22:00
- Finance: peak 09:00-17:00 business hours
- Nutra: relatively flat, slight peak evenings

### Day of Week
- Monday: often lower CR (start-of-week fatigue)
- Friday-Sunday: higher for gambling, dating
- Tuesday-Thursday: higher for B2B, finance
- Weekends: higher for entertainment, lower for business

### Seasonality Flags
- Don't kill campaigns based on 1 bad day
- Compare to same day last week, not yesterday
- Holiday periods may have unusual patterns — wait for normalization

---

## Optimization Workflow

### Daily Routine
1. Check overnight performance → any kill triggers hit?
2. Review top 5 campaigns by spend → ROI trending ok?
3. Check for flows with 0 conversions in 24h
4. Review new test flows → enough data to decide?

### Weekly Routine
1. Full performance review by campaign + flow
2. Kill underperformers, scale winners
3. Launch new A/B tests for top campaigns
4. Review GEO performance — any new GEOs to test?
5. Check domain health and rotate if needed

### Monthly Routine
1. Vertical-level ROI analysis
2. Traffic source performance comparison
3. Offer audit — request better payouts for top offers
4. Clean up dead campaigns, archive unused landings
