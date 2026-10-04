# ============================================
# MODULE 6 : cohort retention analysis
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------
# Load Datasets
# ----------------------------------
customers = pd.read_csv("DATA/saas_customers.csv")
subscriptions = pd.read_csv("DATA/saas_subscriptions.csv")

# ----------------------------------
# Convert Dates
# ----------------------------------
customers["SignupDate"] = pd.to_datetime(customers["SignupDate"])

# ----------------------------------
# Create Cohort Month
# ----------------------------------
customers["CohortMonth"] = customers["SignupDate"].dt.to_period("M")

# ----------------------------------
# Merge Customer and Subscription Data
# ----------------------------------
data = pd.merge(
    customers,
    subscriptions[["CustomerID", "Status"]],
    on="CustomerID",
    how="left"
)

# ----------------------------------
# Count Customers in Each Cohort
# ----------------------------------
cohort_size = data.groupby("CohortMonth")["CustomerID"].nunique()

print("COHORT SIZE")
print(cohort_size)

# ----------------------------------
# Count Active Customers in Cohort
# ----------------------------------
active_customers = (
    data[data["Status"] == "Active"]
    .groupby("CohortMonth")["CustomerID"]
    .nunique()
)

print("\nACTIVE CUSTOMERS")
print(active_customers)

# ----------------------------------
# Retention Percentage
# ----------------------------------
retention = (active_customers / cohort_size) * 100

retention_df = pd.DataFrame({
    "Total_Customers": cohort_size,
    "Active_Customers": active_customers,
    "Retention_Percentage": retention
})

retention_df = retention_df.fillna(0)

print("\nRETENTION TABLE")
print(retention_df)

# ----------------------------------
# Retention Curve
# ----------------------------------
plt.figure(figsize=(10,5))

plt.plot(
    retention_df.index.astype(str),
    retention_df["Retention_Percentage"],
    marker="o"
)

plt.title("Customer Retention by Cohort")
plt.xlabel("Signup Cohort")
plt.ylabel("Retention %")
plt.xticks(rotation=45)
plt.grid(True)

plt.show()

# ----------------------------------
# Best and Worst Cohort
# ----------------------------------
best_cohort = retention_df["Retention_Percentage"].idxmax()
worst_cohort = retention_df["Retention_Percentage"].idxmin()

print("\nBEST COHORT :", best_cohort)
print("BEST RETENTION :", round(retention_df.loc[best_cohort,
      "Retention_Percentage"],2), "%")

print("\nWORST COHORT :", worst_cohort)
print("WORST RETENTION :", round(retention_df.loc[worst_cohort,
      "Retention_Percentage"],2), "%")