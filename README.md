# SkyGeni – Sales Intelligence Decision System
### Project Overview

This project simulates building a Decision Intelligence System for a B2B SaaS company facing declining win rates despite a “healthy” pipeline.

Instead of building a black-box ML model, the focus is on:
- Business problem framing
- Actionable revenue insights
- A white-box risk scoring engine

The goal is to help a CRO answer:
> “What is actually wrong in my pipeline — and what should my team do differently starting today?”

---- 

### My Approach

The solution is structured into five parts:
- **Part 1 - Problem Framing**

  - Identified the core issue as Pipeline Inflation masking Revenue Inefficiency and reframed win rate decline into diagnostic, actionable business questions.

- **Part 2 - Data Exploration & Insights**

  - Performed EDA to uncover:

    1. Declining inbound conversion efficiency

    2. Systemic Q1 market softening

    3. CRM stage discipline inconsistencies

  - Designed two custom metrics:

   1. Deal Velocity Ratio (DVR) - Revenue efficiency per day

   2. Pipeline Rot Index - Aging relative to benchmark win cycle

  - Each insight includes clear business impact and action.

- **Part 3 – White-Box Risk Engine**

  - Built a rule-based scoring engine that:

    - Scores every open deal (0–100)

    - Explains why a deal is risky

    - Prescribes specific actions (PURGE / REVIEW / HEALTHY)

  - This prioritizes interpretability over black-box probability.

- **Part 4 – System Design**

  - Designed a lightweight production architecture:

    - Daily ETL from CRM

    - Weekly benchmark refresh

    - Slack alerts for critical deals

    - Risk score write-back to CRM

    - Manager-focused decision workflow

- **Part 5 – Reflection**

  - Critically examined:

    - Benchmark bias risks

    - Data integrity assumptions

    - Attribution uncertainty

    - Roadmap for next 30 days (segmented benchmarking + activity intelligence)

---- 

### How to Run the Project
**1. Clone the Repository:**
```
git clone https://github.com/aursalan/skygeni.git
cd skygeni
```

**2. Install Dependencies:**
```
pip install pandas numpy matplotlib seaborn
```

**3. Run the Risk Engine:**
```
cd part 3 - build a decision engine
python decision_engine.py
```
This will:

- Train benchmarks on historical closed deals

- Score open pipeline deals

- Generate:
 ```
 skygeni_risk_report.csv
 ```

---- 


### Key Decisions
**1. White-Box Over Black-Box**

Sales leaders need explanations, not probabilities.
Interpretability > marginal accuracy.

**2. Time-Based Train/Test Split**

Used a snapshot date to simulate real-world forecasting conditions.

**3. Rule Calibration from Data**
 - Rules derived from:
   - Historical win rates
   - Benchmark cycle duration
   - Revenue velocity distribution

**4. Operational Focus**
 - The system is designed for:
   - Monday pipeline reviews
   - Manager intervention
   - Forecast cleanup
- Not just dashboard reporting.
