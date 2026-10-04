# ============================================
# MODULE 2 : DATA AUDIT & CLEANING
# ============================================

import pandas as pd

# -----------------------------------------
# Load Datasets
# -----------------------------------------

customers = pd.read_csv("DATA/saas_customers.csv")
subscriptions = pd.read_csv("DATA/saas_subscriptions.csv")
usage = pd.read_csv("DATA/saas_usage.csv")
tickets = pd.read_csv("DATA/saas_tickets.csv")


# -----------------------------------------
# Audit Function
# -----------------------------------------

def audit_dataset(df, name):

    print("\n" + "="*50)
    print("DATASET :", name)
    print("="*50)

    # Shape
    print("\nShape")
    print(df.shape)

    # Data Types
    print("\nData Types")
    print(df.dtypes)

    # Missing Values
    print("\nMissing Values")
    print(df.isnull().sum())

    # Duplicates
    print("\nDuplicate Rows")
    print(df.duplicated().sum())

    # Unique Values in Text Columns
    print("\nUnique Values in Text Columns")

    text_cols = df.select_dtypes(include='object').columns

    for col in text_cols:
        print(f"\nColumn : {col}")
        print(df[col].unique())


# -----------------------------------------
# Run Audit Before Cleaning
# -----------------------------------------

audit_dataset(customers, "Customers")
audit_dataset(subscriptions, "Subscriptions")
audit_dataset(usage, "Usage")
audit_dataset(tickets, "Tickets")


# ============================================
# DATA CLEANING
# ============================================

# -----------------------------------------
# Remove Duplicate Rows
# -----------------------------------------

customers = customers.drop_duplicates()
subscriptions = subscriptions.drop_duplicates()
usage = usage.drop_duplicates()
tickets = tickets.drop_duplicates()


# -----------------------------------------
# Standardize Text Columns
# -----------------------------------------

for col in customers.select_dtypes(include='object').columns:
    customers[col] = customers[col].str.strip().str.title()

for col in subscriptions.select_dtypes(include='object').columns:
    subscriptions[col] = subscriptions[col].str.strip().str.title()

for col in usage.select_dtypes(include='object').columns:
    usage[col] = usage[col].str.strip().str.title()

for col in tickets.select_dtypes(include='object').columns:
    tickets[col] = tickets[col].str.strip().str.title()


# -----------------------------------------
# Handle Missing Values Individually
# -----------------------------------------

customers["Industry"] = customers["Industry"].fillna("Unknown")

customers["AcquisitionChannel"] = customers["AcquisitionChannel"].fillna("Unknown")

customers["EmployeeCount"] = customers["EmployeeCount"].fillna(
    customers["EmployeeCount"].median()
)

subscriptions["Seats"] = subscriptions["Seats"].fillna(
    subscriptions["Seats"].median()
)

subscriptions["MRR"] = subscriptions["MRR"].fillna(
    subscriptions["MRR"].median()
)

usage["ActiveUsers"] = usage["ActiveUsers"].fillna(
    usage["ActiveUsers"].median()
)

usage["SessionMinutes"] = usage["SessionMinutes"].fillna(
    usage["SessionMinutes"].median()
)

tickets["ResolutionHours"] = tickets["ResolutionHours"].fillna(
    tickets["ResolutionHours"].median()
)

tickets["SatisfactionScore"] = tickets["SatisfactionScore"].fillna(
    tickets["SatisfactionScore"].median()
)


# ============================================
# REFERENTIAL INTEGRITY CHECK
# ============================================

print("\nReferential Integrity Check")

valid_customers = customers["CustomerID"]

orphan_subscriptions = subscriptions[
    ~subscriptions["CustomerID"].isin(valid_customers)
]

orphan_usage = usage[
    ~usage["CustomerID"].isin(valid_customers)
]

orphan_tickets = tickets[
    ~tickets["CustomerID"].isin(valid_customers)
]

print("Orphan Records in Subscriptions :", len(orphan_subscriptions))
print("Orphan Records in Usage :", len(orphan_usage))
print("Orphan Records in Tickets :", len(orphan_tickets))


# Remove Orphan Records

subscriptions = subscriptions[
    subscriptions["CustomerID"].isin(valid_customers)
]

usage = usage[
    usage["CustomerID"].isin(valid_customers)
]

tickets = tickets[
    tickets["CustomerID"].isin(valid_customers)
]


# ============================================
# RE-RUN AUDIT AFTER CLEANING
# ============================================

print("\n\nAFTER CLEANING")

audit_dataset(customers, "Customers")
audit_dataset(subscriptions, "Subscriptions")
audit_dataset(usage, "Usage")
audit_dataset(tickets, "Tickets")


# ============================================
# SAVE CLEANED FILES
# ============================================

customers.to_csv("clean_customers.csv", index=False)

subscriptions.to_csv("clean_subscriptions.csv", index=False)

usage.to_csv("clean_usage.csv", index=False)

tickets.to_csv("clean_tickets.csv", index=False)

print("\nCleaning Completed Successfully")