# ============================================
# MODULE 4 : PANDAS WRANGLING & EDA
# ============================================

import pandas as pd
import numpy as np

# Load datasets
customers = pd.read_csv("DATA/clean_customers.csv")
subscriptions = pd.read_csv("DATA/clean_subscriptions.csv")
usage = pd.read_csv("DATA/clean_usage.csv")
tickets = pd.read_csv("DATA/clean_tickets.csv")
# -------------------------
# Merge Datasets
# -------------------------

merged = pd.merge(customers, subscriptions,
                  on="CustomerID",
                  how="left")

usage_summary = usage.groupby("CustomerID").agg({
    "Logins": "mean",
    "ActiveUsers": "mean",
    "APICalls": "mean"
}).reset_index()

merged = pd.merge(merged, usage_summary,
                  on="CustomerID",
                  how="left")

ticket_summary = tickets.groupby("CustomerID").agg({
    "TicketID": "count"
}).reset_index()

ticket_summary.rename(
    columns={"TicketID": "TotalTickets"},
    inplace=True
)

merged = pd.merge(merged, ticket_summary,
                  on="CustomerID",
                  how="left")

# -------------------------
# Calculated Columns
# -------------------------

merged["SignupDate"] = pd.to_datetime(merged["SignupDate"])

today = pd.Timestamp.today()

merged["Tenure_Months"] = (
    (today - merged["SignupDate"]).dt.days / 30
).round(1)

merged["Revenue_Per_Seat"] = (
    merged["MRR"] / merged["Seats"]
)

merged["Tickets_Per_Month"] = (
    merged["TotalTickets"] /
    merged["Tenure_Months"]
)

# -------------------------
# GroupBy Analysis
# -------------------------

industry_summary = merged.groupby("Industry").agg({
    "MRR": ["sum", "mean"],
    "CustomerID": "count"
})

print("\ngroupby Analysis:")
print(industry_summary)

# -------------------------
# Pivot Table
# -------------------------

pivot = pd.pivot_table(
    merged,
    values="MRR",
    index="Industry",
    columns="PlanName",
    aggfunc="mean"
)

print("\nPivot Table:")
print(pivot)

# -------------------------
# IQR Outlier Detection
# -------------------------

Q1 = merged["MRR"].quantile(0.25)
Q3 = merged["MRR"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - (1.5 * IQR)
upper_limit = Q3 + (1.5 * IQR)

outliers = merged[
    (merged["MRR"] < lower_limit) |
    (merged["MRR"] > upper_limit)
]

print("\nOutliers:")
print(outliers[["CustomerID", "MRR"]])

# -------------------------
# Correlation Matrix
# -------------------------

corr_matrix = merged[
    ["MRR",
     "Seats",
     "Logins",
     "ActiveUsers",
     "APICalls"]
].corr()

print("\nCorrelation Matrix:")
print(corr_matrix)
