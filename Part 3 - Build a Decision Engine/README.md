# 1. Define the Problem Clearly
**The CRO’s core issue is Pipeline Inflation.**

While the "Total Pipeline Value" looks healthy on paper, our analysis in Part 2 revealed that open deals are "Zombies" (rotting in the pipeline) and Inbound leads from Q4 2023 have less win rate (significantly below the 50% benchmark).
The sales team is wasting time working on deals that are statistically dead, and the revenue forecast is inaccurate because it treats these high-risk deals as "healthy."

**The Goal:** We need a system to objectively score every open deal’s likelihood of failure so we can purge the bad deals and focus on the good ones. 

----

# 2. The Solution: A White-Box Risk Engine
**Instead of a "Black Box" Machine Learning model (which gives a probability like 0.82 but no explanation), we built a White-Box Rule Engine.**

Our engine calculates a Risk Score (0–100) based on four deterministic business rules derived from our data analysis:
- **Rule 1:** The Zombie Check (Rot Index)
  - Logic: If a deal has been open 1.5x the average winning cycle (94 days), it is penalized heavily (+50 Risk).
  - Why: History shows these deals almost never close.
- **Rule 2:** The Cohort Trap (Lead Quality)
  - Logic: If a deal comes from a cohort with a historical win rate <45 (e.g., Inbound Q4 2023), it gets a penalty (+25 Risk).
  - Why: This protects the forecast from low-quality marketing leads.
- **Rule 3:** Revenue Velocity (Economics)
  - Logic: If a deal is generating $345/day in potential velocity (half the benchmark), it is flagged (+20 Risk).
  - Why: These deals are inefficient "time sinks" for reps.
- **Rule 4:** Process Hygiene (Compliance)
  - Logic: If a deal is in 'Demo' stage for +30 days, it is flagged (+30 Risk).
  - Why: This indicates the rep is not updating the CRM or the deal is stalled.

----

# 3. Actionable Outputs
The system generates a CSV report `skygeni_decision_engine_report.csv` that doesn't just list problems, it prescribes Actions.

----

# 4. How a Sales Leader Would Use This
The SkyGeni Risk Engine replaces subjective "gut feelings" with a data-driven protocol, turning the weekly pipeline review into a focused strategy session.

### Phase 1: The "Purge" Protocol (5 Minutes)
**Goal:** Eliminate forecast noise and "Zombie" deals.

**Action:** Filter the output report for Action = PURGE (High Risk).

**The Play:** "These deals are statistically dead (Rot Index > 1.5). Unless a meeting is booked on the calendar for this week, they are moved to 'Closed-Lost' immediately."

**Result:** Instantly cleans the revenue forecast by removing deals that historically have a <5% chance of closing.

### Phase 2: The "Save" Protocol (20 Minutes)
**Goal:** Unblock stalled deals that are still winnable.

**Action:** Filter the output report for Action = REVIEW (Medium Risk).

**The Play:** Focus coaching efforts here. "This deal is stalled in 'Demo' stage (Risk Score: 50+). Do we need an Executive Sponsor to unstuck it? What is the specific blocker?"

**Result:** Managers spend time coaching on deals that matter, rather than interrogating reps about dead leads.
