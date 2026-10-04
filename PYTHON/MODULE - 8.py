# ==========================================================
# MODULE 8 - CUSTOMER SEGMENTATION
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# ==========================================================
# LOAD DATASETS
# ==========================================================

subscriptions = pd.read_csv("DATA/clean_subscriptions.csv")
usage = pd.read_csv("DATA/clean_usage.csv")

# ==========================================================
# CREATE CUSTOMER LEVEL FEATURES
# ==========================================================

customer_features = usage.groupby("CustomerID").agg({
    "Logins": "mean",
    "ActiveUsers": "mean",
    "APICalls": "mean",
    "SessionMinutes": "mean"
}).reset_index()

# ==========================================================
# MERGE SUBSCRIPTION DATA
# ==========================================================

customer_features = pd.merge(
    customer_features,
    subscriptions[["CustomerID", "MRR", "Seats"]],
    on="CustomerID",
    how="left"
)

# ==========================================================
# HANDLE MISSING VALUES
# ==========================================================

numeric_columns = [
    "Logins",
    "ActiveUsers",
    "APICalls",
    "SessionMinutes",
    "MRR",
    "Seats"
]

for col in numeric_columns:
    customer_features[col] = pd.to_numeric(
        customer_features[col],
        errors="coerce"
    )

for col in numeric_columns:
    customer_features[col] = customer_features[col].fillna(
        customer_features[col].median()
    )

# ==========================================================
# VERIFY MISSING VALUES
# ==========================================================

print("\nMissing Values Check")
print(customer_features[numeric_columns].isnull().sum())

# Extra safety
customer_features = customer_features.dropna(
    subset=numeric_columns
)

# ==========================================================
# FEATURE MATRIX
# ==========================================================

X = customer_features[numeric_columns]

# ==========================================================
# SCALE FEATURES
# ==========================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ==========================================================
# ELBOW METHOD
# ==========================================================

wcss = []

for k in range(1, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    wcss.append(model.inertia_)

plt.figure(figsize=(8,5))

plt.plot(
    range(1,11),
    wcss,
    marker="o"
)

plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")

plt.show()

# ==========================================================
# APPLY KMEANS
# ==========================================================

kmeans = KMeans(
    n_clusters=4,
    random_state=42,
    n_init=10
)

customer_features["Cluster"] = (
    kmeans.fit_predict(X_scaled)
)

# ==========================================================
# CLUSTER SUMMARY
# ==========================================================

cluster_summary = customer_features.groupby("Cluster")[
    numeric_columns
].mean()

print("\nCluster Summary")
print(cluster_summary)

# ==========================================================
# CLUSTER NAMES
# ==========================================================

cluster_names = {
    0: "Power Users",
    1: "High Value Customers",
    2: "At Risk Customers",
    3: "Moderate Users"
}

customer_features["Segment"] = customer_features[
    "Cluster"
].map(cluster_names)

# ==========================================================
# SEGMENT COUNT
# ==========================================================

segment_count = customer_features[
    "Segment"
].value_counts()

print("\nCustomers in Each Segment")
print(segment_count)

# ==========================================================
# BAR CHART
# ==========================================================

plt.figure(figsize=(8,5))

segment_count.plot(
    kind="bar",
    color="skyblue"
)

plt.title("Customer Segments")
plt.xlabel("Segment")
plt.ylabel("Customer Count")

plt.show()

# ==========================================================
# EXPORT RESULT
# ==========================================================

customer_features.to_csv(
    "customer_segmentation.csv",
    index=False
)

print("\nModule 8 Completed Successfully")
