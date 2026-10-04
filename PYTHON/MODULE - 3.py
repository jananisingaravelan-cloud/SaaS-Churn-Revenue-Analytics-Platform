# ============================================
# MODULE 3 : NUMPY
# ============================================

import pandas as pd
import numpy as np

# Load datasets
subscriptions = pd.read_csv("DATA/saas_subscriptions.csv")
usage = pd.read_csv("DATA/saas_usage.csv")

# Handle missing values
subscriptions["MRR"] = subscriptions["MRR"].fillna(0)
subscriptions["Seats"] = subscriptions["Seats"].fillna(0)
usage["Logins"] = usage["Logins"].fillna(0)

# Convert columns to NumPy arrays
mrr_array = subscriptions["MRR"].to_numpy()
seats_array = subscriptions["Seats"].to_numpy()
logins_array = usage["Logins"].to_numpy()

# -------------------------
# MRR Statistics
# -------------------------
print("MRR Statistics")
print("Mean:", np.mean(mrr_array))
print("Standard Deviation:", np.std(mrr_array))
print("Minimum:", np.min(mrr_array))
print("Maximum:", np.max(mrr_array))

# -------------------------
# Seats Statistics
# -------------------------
print("\nSeats Statistics")
print("Mean:", np.mean(seats_array))
print("Standard Deviation:", np.std(seats_array))
print("Minimum:", np.min(seats_array))
print("Maximum:", np.max(seats_array))

# -------------------------
# Logins Statistics
# -------------------------
print("\nLogins Statistics")
print("Mean:", np.mean(logins_array))
print("Standard Deviation:", np.std(logins_array))
print("Minimum:", np.min(logins_array))
print("Maximum:", np.max(logins_array))

# -------------------------
# Normalize MRR
# -------------------------
subscriptions["Normalized_MRR"] = (
    (subscriptions["MRR"] - np.min(mrr_array))
    / (np.max(mrr_array) - np.min(mrr_array))
)

# -------------------------
# High Value Customers
# -------------------------
subscriptions["High_Value"] = np.where(
    subscriptions["MRR"] > 1000,
    "Yes",
    "No"
)

# -------------------------
# At Risk Customers
# -------------------------
subscriptions["At_Risk"] = np.where(
    (subscriptions["Status"] == "Churned") |
    (subscriptions["MRR"] < 100),
    "Yes",
    "No"
)

# Display Results

print("\nCustomer Flags")
print(subscriptions[[
    "CustomerID",
    "MRR",
    "Normalized_MRR",
    "High_Value",
    "At_Risk"
]].head(10))