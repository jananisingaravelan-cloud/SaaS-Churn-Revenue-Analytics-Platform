# ==========================================================
# MODULE 9 - CHURN RISK SCORING
# ==========================================================

import pandas as pd

# ==========================================================
# LOAD DATASETS
# ==========================================================

usage = pd.read_csv("DATA/saas_usage.csv")
subscriptions = pd.read_csv("DATA/saas_subscriptions.csv")
tickets = pd.read_csv("DATA/saas_tickets.csv")

# ==========================================================
# CUSTOMER LEVEL USAGE FEATURES
# ==========================================================

usage_summary = usage.groupby("CustomerID").agg({
    "Logins": "mean",
    "ActiveUsers": "mean",
    "SessionMinutes": "mean"
}).reset_index()

# ==========================================================
# CUSTOMER LEVEL TICKET FEATURES
# ==========================================================

ticket_summary = tickets.groupby("CustomerID").agg({
    "SatisfactionScore": "mean"
}).reset_index()

# ==========================================================
# MERGE DATASETS
# ==========================================================

risk_data = pd.merge(
    subscriptions,
    usage_summary,
    on="CustomerID",
    how="left"
)

risk_data = pd.merge(
    risk_data,
    ticket_summary,
    on="CustomerID",
    how="left"
)

# ==========================================================
# HANDLE MISSING VALUES 
# ==========================================================

risk_data["Logins"] = risk_data["Logins"].fillna(
    risk_data["Logins"].median()
)

risk_data["ActiveUsers"] = risk_data["ActiveUsers"].fillna(
    risk_data["ActiveUsers"].median()
)

risk_data["SessionMinutes"] = risk_data["SessionMinutes"].fillna(
    risk_data["SessionMinutes"].median()
)

risk_data["SatisfactionScore"] = risk_data["SatisfactionScore"].fillna(
    risk_data["SatisfactionScore"].median()
)

risk_data["MRR"] = risk_data["MRR"].fillna(
    risk_data["MRR"].median()
)

# ==========================================================
# CREATE RISK SCORE
# ==========================================================

risk_data["RiskScore"] = 0

# Low Login Activity
risk_data.loc[
    risk_data["Logins"] < 5,
    "RiskScore"
] += 25

# Low Active Users
risk_data.loc[
    risk_data["ActiveUsers"] < 3,
    "RiskScore"
] += 25

# Low Session Time
risk_data.loc[
    risk_data["SessionMinutes"] < 100,
    "RiskScore"
] += 25

# Low Satisfaction
risk_data.loc[
    risk_data["SatisfactionScore"] < 5,
    "RiskScore"
] += 25

# ==========================================================
# CREATE RISK CATEGORY
# ==========================================================

risk_data["RiskCategory"] = "Low Risk"

risk_data.loc[
    risk_data["RiskScore"] >= 50,
    "RiskCategory"
] = "Medium Risk"

risk_data.loc[
    risk_data["RiskScore"] >= 75,
    "RiskCategory"
] = "High Risk"

# ==========================================================
# CUSTOMER RANKING
# ==========================================================

risk_ranking = risk_data.sort_values(
    by="RiskScore",
    ascending=False
)

# ==========================================================
# TOP 20 HIGH RISK CUSTOMERS
# ==========================================================

print("\nTOP 20 HIGH RISK CUSTOMERS")

print(
    risk_ranking[
        [
            "CustomerID",
            "MRR",
            "RiskScore",
            "RiskCategory"
        ]
    ].head(20)
)

# ==========================================================
# MRR IN HIGH RISK GROUP
# ==========================================================

high_risk_mrr = risk_data[
    risk_data["RiskCategory"] == "High Risk"
]["MRR"].sum()

print("\nTOTAL MRR IN HIGH RISK GROUP")
print(round(high_risk_mrr, 2))

# ==========================================================
# CUSTOMER COUNT BY RISK CATEGORY
# ==========================================================

risk_count = risk_data[
    "RiskCategory"
].value_counts()

print("\nCUSTOMER COUNT BY RISK CATEGORY")
print(risk_count)

# ==========================================================
# SAVE OUTPUT
# ==========================================================

risk_ranking.to_csv(
    "churn_risk_scores.csv",
    index=False
)

print("\nModule 9 Completed Successfully")