# ==========================================================
# MODULE 7 - VISUALIZATION
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# LOAD DATASETS
# ==========================================================

customers = pd.read_csv("DATA/saas_customers.csv")
subscriptions = pd.read_csv("DATA/saas_subscriptions.csv")
usage = pd.read_csv("DATA/saas_usage.csv")
tickets = pd.read_csv("DATA/saas_tickets.csv")

sns.set_style("whitegrid")

# ==========================================================
# CHART 1 - CHURN TREND OVER TIME
# ==========================================================

subscriptions["EndDate"] = pd.to_datetime(
    subscriptions["EndDate"],
    errors="coerce"
)

churned = subscriptions[
    subscriptions["Status"] == "Churned"
]

churn_trend = churned.groupby(
    churned["EndDate"].dt.to_period("M")
).size()

plt.figure(figsize=(10,5))
churn_trend.plot(marker="o", color="red")

plt.title("Churn Trend Over Time")
plt.xlabel("Month")
plt.ylabel("Number of Churned Customers")
plt.grid(True)

plt.show()

# ==========================================================
# CHART 2 - RETENTION CURVE
# ==========================================================

customers["SignupDate"] = pd.to_datetime(
    customers["SignupDate"]
)

cohort_data = pd.merge(
    customers,
    subscriptions[["CustomerID", "Status"]],
    on="CustomerID",
    how="left"
)

cohort_size = (
    cohort_data.groupby(
        cohort_data["SignupDate"].dt.to_period("M")
    )["CustomerID"]
    .count()
)

active_customers = (
    cohort_data[
        cohort_data["Status"] == "Active"
    ]
    .groupby(
        cohort_data["SignupDate"].dt.to_period("M")
    )["CustomerID"]
    .count()
)

retention = (
    active_customers / cohort_size
) * 100

plt.figure(figsize=(10,5))
retention.plot(marker="o", color="green")

plt.title("Retention Curve")
plt.xlabel("Signup Cohort")
plt.ylabel("Retention Percentage")
plt.grid(True)

plt.show()

# ==========================================================
# CHART 3 - CHURN BY SEGMENT
# ==========================================================

segment_data = pd.merge(
    customers,
    subscriptions[["CustomerID", "Status"]],
    on="CustomerID"
)

segment_churn = pd.crosstab(
    segment_data["Industry"],
    segment_data["Status"]
)

segment_churn.plot(
    kind="bar",
    figsize=(12,6)
)

plt.title("Churn By Segment")
plt.xlabel("Industry")
plt.ylabel("Customer Count")
plt.xticks(rotation=45)

plt.show()

# ==========================================================
# CHART 4 - USAGE DISTRIBUTION
# ==========================================================

plt.figure(figsize=(10,5))

sns.histplot(
    usage["Logins"],
    bins=20,
    kde=True,
    color="skyblue"
)

plt.title("Usage Distribution")
plt.xlabel("Logins")
plt.ylabel("Frequency")

plt.show()

# ==========================================================
# CHART 5 - USAGE VS CHURN RELATIONSHIP
# ==========================================================

usage_status = pd.merge(
    usage,
    subscriptions[["CustomerID", "Status"]],
    on="CustomerID"
)

plt.figure(figsize=(8,5))

sns.boxplot(
    x="Status",
    y="Logins",
    data=usage_status
)

plt.title("Usage vs Churn Relationship")
plt.xlabel("Customer Status")
plt.ylabel("Logins")

plt.show()

# ==========================================================
# CHART 6 - TICKET SATISFACTION IMPACT
# ==========================================================

ticket_status = pd.merge(
    tickets,
    subscriptions[["CustomerID", "Status"]],
    on="CustomerID",
    how="left"
)

plt.figure(figsize=(8,5))

sns.boxplot(
    x="Status",
    y="SatisfactionScore",
    data=ticket_status
)

plt.title("Ticket Satisfaction Impact")
plt.xlabel("Customer Status")
plt.ylabel("Satisfaction Score")

plt.show()

# ==========================================================
# CHART 7 - CORRELATION HEATMAP
# ==========================================================

merged_data = pd.merge(
    usage,
    subscriptions[
        ["CustomerID", "MRR", "Seats"]
    ],
    on="CustomerID",
    how="left"
)

numeric_columns = [
    "Logins",
    "ActiveUsers",
    "APICalls",
    "SessionMinutes",
    "MRR",
    "Seats"
]

correlation = (
    merged_data[numeric_columns]
    .corr()
)

plt.figure(figsize=(10,6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.show()

print("Module 7 Completed Successfully")