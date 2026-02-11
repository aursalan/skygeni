# 1. What assumptions in your solution are weakest?
- **The "One-Size-Fits-All" Benchmark:** The system uses a global average of 63 days for the Rot Index. In reality, a $100k Enterprise deal naturally has a longer sales cycle than a $5k SMB deal. Using a single benchmark risks "false positives," where healthy, high-value deals are flagged as Zombies simply because they are complex and require more time.
- **Historical Accuracy (The Sandbagging Risk):** The engine assumes that the closed_date in the dataset represents the actual moment a deal ended. However, sales reps often "batch-close" lost deals on the final day of a quarter to avoid mid-quarter scrutiny. If the historical data is "polluted" by this behavior, the benchmarks for what constitutes a "normal" cycle are artificially inflated.

----

# 2. What would break in real-world production?
- **The "Cold Start" for New Initiatives:** Cohort Win Rate depends entirely on historical performance. If the company launches a brand-new product line or enters a new geographic region next week, the system will have zero win-rate data to reference. The engine would effectively be "blind" to the risks of these new strategic initiatives for the first 3–6 months.
- **API Rate Limits & Data Volume:** The current design assumes a nightly "Full Extract" of all deals. If the pipeline scales to 100,000+ open deals, this process will likely hit Salesforce/HubSpot API rate limits or cause significant latency in the ETL worker. A production version would require a more complex "Incremental Sync" to only fetch records modified in the last 24 hours.

----

# 3. What would you build next if given 1 month?
- **Segmented Benchmarking:** I would upgrade the engine to calculate dynamic benchmarks based on Product_Type and Deal_Amount. This would ensure that a $50k Enterprise deal is compared against other $50k deals, rather than being unfairly penalized by the speed of $2k Core deals.
- **Activity-Based Intelligence:** Rules-based systems are limited to CRM fields. I would integrate a "Sidecar" that pulls metadata from Gmail/Outlook and Calendar APIs. If a deal is 90 days old (Zombie) but had three meetings and 15 emails in the last 48 hours, the system should automatically "waive" the penalty because of high real-time engagement.
- **Macro-Economic Weighting:** Sales win rates are often influenced by external factors (e.g., high interest rates or industry-specific downturns). I would allow the Sales Leader to manually "weight" specific industries to increase or decrease risk scores based on current market conditions.

----

# 4. What part of your solution are you least confident about?
**The "Attribution" of the Cohort Dip:** In Part 2, we identified that "Inbound 2024Q1" leads had a win rate of only 41%. We built a rule to penalize these leads. However, the data doesn't tell us why the rate dropped. It could be that the marketing leads were low quality, but it could also be that a group of new, inexperienced reps was assigned to that cohort. I am least confident that we are penalizing the right variable; we might be blaming the "Lead Source" for what is actually a "Sales Training" issue.
