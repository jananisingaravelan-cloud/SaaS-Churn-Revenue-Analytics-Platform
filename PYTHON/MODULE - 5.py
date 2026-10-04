# ============================================
# MODULE 5 : statistics
# ============================================

import pandas as pd
from scipy import stats

# Load datasets
usage = pd.read_csv("DATA/saas_usage.csv")
subscriptions = pd.read_csv("DATA/saas_subscriptions.csv")

# -----------------------------
# Merge data
# -----------------------------
data = pd.merge(
    usage,
    subscriptions[["CustomerID", "Status"]],
    on="CustomerID",
    how="left"
)

# -----------------------------
# 1. Descriptive Statistics
# -----------------------------
print("DESCRIPTIVE STATISTICS")
print(data["Logins"].describe())

# Additional metrics
print("\nAverage Logins:", data["Logins"].mean())
print("Median Logins:", data["Logins"].median())
print("Standard Deviation:", data["Logins"].std())

# -----------------------------
# 2. Random Sample Comparison
# -----------------------------
sample1 = data["Logins"].sample(30, random_state=1)
sample2 = data["Logins"].sample(30, random_state=2)

population_mean = data["Logins"].mean()

print("\nSAMPLE COMPARISON")
print("Population Mean:", round(population_mean, 2))
print("Sample 1 Mean:", round(sample1.mean(), 2))
print("Sample 2 Mean:", round(sample2.mean(), 2))

# -----------------------------
# 3. Hypothesis Test
# H0: Churned and Active customers
# have the same average login count
# -----------------------------
churned = data[data["Status"] == "Churned"]["Logins"]
active = data[data["Status"] == "Active"]["Logins"]

t_stat, p_value = stats.ttest_ind(
    churned,
    active,
    nan_policy="omit"
)

print("\nHYPOTHESIS TEST")
print("T Statistic:", round(t_stat, 4))
print("P Value:", round(p_value, 4))

# -----------------------------
# 4. Interpretation
# -----------------------------
alpha = 0.05

if p_value < alpha:
    print("\nResult: Reject the Null Hypothesis")
    print("There is a significant difference in login activity.")
else:
    print("\nResult: Fail to Reject the Null Hypothesis")
    print("No significant difference was found.")