import pandas as pd
import numpy as np

SNAPSHOT_DATE = pd.Timestamp('2024-01-01')

class SkyGeniRiskEngine:
    """
    OPTION A: Deal Risk Scoring System
    """
    
    def __init__(self):
        self.benchmark_days = 0
        self.benchmark_velocity = 0
        self.cohort_win_rates = {}
        self.risky_cohorts = []

    def fit(self, historical_df):
        print(f"\n--- 1. LEARNING PHASE (Data before {SNAPSHOT_DATE.date()}) ---")
        
        won_deals = historical_df[historical_df['outcome'].str.lower() == 'won'].copy()
        
        won_deals['actual_days'] = (won_deals['closed_date'] - won_deals['created_date']).dt.days.replace(0, 1)
        won_deals['velocity'] = won_deals['deal_amount'] / won_deals['actual_days']
        
        self.benchmark_days = won_deals['actual_days'].mean()
        self.benchmark_velocity = won_deals['velocity'].mean()
        
        print(f"Benchmarks Established:")
        print(f" - Avg Time to Win: {self.benchmark_days:.1f} days")
        print(f" - Avg Revenue Velocity: ${self.benchmark_velocity:.2f}/day")

        historical_df['cohort'] = historical_df['created_date'].dt.to_period('Q').astype(str)

        cohort_stats = historical_df.groupby(['cohort', 'lead_source'])['outcome'].apply(
            lambda x: (x.str.lower()=='won').mean()
        )

        self.cohort_win_rates = cohort_stats.to_dict()

        cohort_matrix = historical_df.pivot_table(
            index='lead_source', 
            columns='cohort', 
            values='outcome', 
            aggfunc=lambda x: (x.str.lower()=='won').mean()
        )
        
        print("\n--- COHORT WIN RATE (Lead Source vs Cohort) ---")
        print(cohort_matrix.round(2).to_string())

        self.risky_cohorts = cohort_stats[cohort_stats < 0.45].index.tolist()
        
        print(f"\n Risky Segments Identified (<45% Win Rate): {len(self.risky_cohorts)}")


    def score_deal(self, row):
        score = 0

        rot_index = row['rot_index']
        curr_velocity = row['deal_velocity_ratio']
        days_open = row['current_cycle_days']
        win_rate = row['cohort_win_rate']

        if rot_index > 1.5: score += 50
        elif rot_index > 1.2: score += 20

        if curr_velocity < (self.benchmark_velocity * 0.5): score += 20

        if win_rate < 0.45: score += 25

        if row['deal_stage'] == 'Demo' and days_open > 30: score += 30

        final_score = min(score, 100)

        if final_score >= 80: action = "PURGE (High Risk)"
        elif final_score >= 50: action = "REVIEW (Medium Risk)"
        else: action = "HEALTHY"
        
        return pd.Series([final_score, action])

    def predict(self, open_deals_df):
        print(f"\n--- 2. SCORING PHASE (Simulating {len(open_deals_df)} Open Deals) ---")

        open_deals_df['current_cycle_days'] = (SNAPSHOT_DATE - open_deals_df['created_date']).dt.days.replace(0, 1)
        open_deals_df['rot_index'] = open_deals_df['current_cycle_days'] / self.benchmark_days
        open_deals_df['deal_velocity_ratio'] = open_deals_df['deal_amount'] / open_deals_df['current_cycle_days']

        open_deals_df['cohort_temp'] = open_deals_df['created_date'].dt.to_period('Q').astype(str)
        
        open_deals_df['cohort_win_rate'] = open_deals_df.apply(
            lambda x: self.cohort_win_rates.get((x['cohort_temp'], x['lead_source']), 0.5), 
            axis=1
        )
        
        results = open_deals_df.apply(self.score_deal, axis=1)
        results.columns = ['risk_score', 'action']
        
        return pd.concat([open_deals_df, results], axis=1)

df = pd.read_csv('skygeni_sales_data.csv')
df['created_date'] = pd.to_datetime(df['created_date'])
df['closed_date'] = pd.to_datetime(df['closed_date'])

train_df = df[df['closed_date'] < SNAPSHOT_DATE].copy()
open_pipeline = df[
    (df['created_date'] < SNAPSHOT_DATE) & 
    (df['closed_date'] >= SNAPSHOT_DATE)
].copy()

engine = SkyGeniRiskEngine()
engine.fit(train_df)
scored_pipeline = engine.predict(open_pipeline)

final_report = scored_pipeline[[
    'deal_id', 'created_date', 'sales_rep_id', 
    'rot_index', 'deal_velocity_ratio', 'current_cycle_days', 
    'deal_stage', 'cohort_win_rate', 'risk_score', 'action'
]].copy()
final_report.rename(columns={'sales_rep_id': 'sales_reps_id'}, inplace=True)
final_report.sort_values('risk_score', ascending=False, inplace=True)

final_report.to_csv('skygeni_decision_engine_report.csv', index=False)
print("\n--- REPORT GENERATED: skygeni_decision_engine_report.csv ---\n")