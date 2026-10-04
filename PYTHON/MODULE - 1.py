#============================================
# SaaS CHURN & REVENUE ANALYTICS PLATFORM
#============================================

import pandas as pd

#============================================
# MODULE - 1 : PYTHON FOUNDATION
#============================================

# -----------------------------------------
# Load File
# -----------------------------------------
def load_file(file_name):
    try:
        df = pd.read_csv(file_name)
        print(f"{file_name} loaded successfully")
        return df

    except FileNotFoundError:
        print(f"{file_name} not found")

    except Exception as e:
        print("Error :", e)


# -----------------------------------------
# Utility Function 1 - Dataset Shape
# -----------------------------------------
def show_shape(df, name):
    print("\nDataset :", name)
    print("Rows :", df.shape[0])
    print("Columns :", df.shape[1])


# -----------------------------------------
# Utility Function 2 - Dataset Columns
# -----------------------------------------
def show_columns(df, name):
    print("\nColumns in", name)
    print(df.columns.tolist())


# -----------------------------------------
# Utility Function 3 - Data Types
# -----------------------------------------
def show_dtypes(df, name):
    print("\nData Types in", name)
    print(df.dtypes)


# -----------------------------------------
# Load All Files
# -----------------------------------------

customers = load_file("DATA/saas_customers.csv")
subscriptions = load_file("DATA/saas_subscriptions.csv")
usage = load_file("DATA/saas_usage.csv")
tickets = load_file("DATA/saas_tickets.csv")


# -----------------------------------------
# Validate Customer File
# -----------------------------------------

show_shape(customers, "Customers")
show_columns(customers, "Customers")
show_dtypes(customers, "Customers")


# -----------------------------------------
# Validate Subscription File
# -----------------------------------------

show_shape(subscriptions, "Subscriptions")
show_columns(subscriptions, "Subscriptions")
show_dtypes(subscriptions, "Subscriptions")


# -----------------------------------------
# Validate Usage File
# -----------------------------------------

show_shape(usage, "Usage")
show_columns(usage, "Usage")
show_dtypes(usage, "Usage")


# -----------------------------------------
# Validate Tickets File
# -----------------------------------------

show_shape(tickets, "Tickets")
show_columns(tickets, "Tickets")
show_dtypes(tickets, "Tickets")


# -----------------------------------------
# Display First 5 Rows
# -----------------------------------------

print("\nCustomers Data")
print(customers.head())

print("\nSubscriptions Data")
print(subscriptions.head())

print("\nUsage Data")
print(usage.head())

print("\nTickets Data")
print(tickets.head())

print("\nAll files loaded and validated successfully")


