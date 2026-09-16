import pandas as pd

# Load historical processed delivery data
df = pd.read_csv(
    "data/processed/delivery_dataset.csv"
)

print("Dataset loaded successfully")
print("Rows:", len(df))
print("Unique orders:", df["order_id"].nunique())

# Create one row per unique order
orders = df[
    [
        "order_id",
        "customer_state",
        "is_late"
    ]
].drop_duplicates("order_id")

# Convert date columns to datetime
df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

df["order_delivered_customer_date"] = pd.to_datetime(
    df["order_delivered_customer_date"]
)

# Calculate delivery duration in days
df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Calculate overall late delivery rate
total_orders = len(orders)
late_orders = orders["is_late"].sum()
late_rate = (late_orders / total_orders) * 100

print("\n--- Overall Delivery Performance ---")
print("Total orders:", total_orders)
print("Late orders:", late_orders)
print(f"Late delivery rate: {late_rate:.2f}%")


# Create one row per order for delivery time analysis
delivery_time_orders = df[
    [
        "order_id",
        "delivery_days"
    ]
].drop_duplicates("order_id")

average_delivery_days = delivery_time_orders["delivery_days"].mean()
median_delivery_days = delivery_time_orders["delivery_days"].median()

print("\n--- Delivery Time Performance ---")
print(f"Average delivery time: {average_delivery_days:.2f} days")
print(f"Median delivery time: {median_delivery_days:.2f} days")

# Analyze late delivery by customer state
customer_state_analysis = orders.groupby("customer_state").agg(
    total_orders=("order_id", "count"),
    late_orders=("is_late", "sum"),
    late_rate=("is_late", "mean")
).reset_index()

customer_state_analysis["late_rate"] = (
    customer_state_analysis["late_rate"] * 100
)

customer_state_analysis = customer_state_analysis.sort_values(
    "late_rate",
    ascending=False
)

print("\n--- Late Delivery by Customer State ---")
print(customer_state_analysis.head(10))

# Create unique order + seller state combinations
seller_orders = df[
    [
        "order_id",
        "seller_state",
        "is_late"
    ]
].drop_duplicates(
    ["order_id", "seller_state"]
)

# Analyze late delivery by seller state
seller_state_analysis = seller_orders.groupby("seller_state").agg(
    total_orders=("order_id", "count"),
    late_orders=("is_late", "sum"),
    late_rate=("is_late", "mean")
).reset_index()

seller_state_analysis["late_rate"] = (
    seller_state_analysis["late_rate"] * 100
)

# Keep seller states with at least 100 orders
seller_state_analysis = seller_state_analysis[
    seller_state_analysis["total_orders"] >= 100
]

seller_state_analysis = seller_state_analysis.sort_values(
    "late_rate",
    ascending=False
)

print("\n--- Late Delivery by Seller State ---")
print(seller_state_analysis)

# Create one row per order for customer delivery time analysis
customer_delivery_time = df[
    [
        "order_id",
        "customer_state",
        "delivery_days"
    ]
].drop_duplicates("order_id")

# Calculate delivery time by customer state
customer_delivery_analysis = customer_delivery_time.groupby(
    "customer_state"
).agg(
    total_orders=("order_id", "count"),
    average_delivery_days=("delivery_days", "mean"),
    median_delivery_days=("delivery_days", "median")
).reset_index()

customer_delivery_analysis = customer_delivery_analysis.sort_values(
    "average_delivery_days",
    ascending=False
)

print("\n--- Delivery Time by Customer State ---")
print(customer_delivery_analysis.head(10))

# Create unique order + seller state combinations
seller_delivery_time = df[
    [
        "order_id",
        "seller_state",
        "delivery_days"
    ]
].drop_duplicates(
    ["order_id", "seller_state"]
)

# Calculate delivery time by seller state
seller_delivery_analysis = seller_delivery_time.groupby(
    "seller_state"
).agg(
    total_orders=("order_id", "count"),
    average_delivery_days=("delivery_days", "mean"),
    median_delivery_days=("delivery_days", "median")
).reset_index()

# Keep seller states with at least 100 orders
seller_delivery_analysis = seller_delivery_analysis[
    seller_delivery_analysis["total_orders"] >= 100
]

seller_delivery_analysis = seller_delivery_analysis.sort_values(
    "average_delivery_days",
    ascending=False
)

print("\n--- Delivery Time by Seller State ---")
print(seller_delivery_analysis)

# Save analytics results for future dashboard use
customer_state_analysis.to_csv(
    "data/processed/customer_state_analysis.csv",
    index=False
)

seller_state_analysis.to_csv(
    "data/processed/seller_state_analysis.csv",
    index=False
)

customer_delivery_analysis.to_csv(
    "data/processed/customer_delivery_analysis.csv",
    index=False
)

seller_delivery_analysis.to_csv(
    "data/processed/seller_delivery_analysis.csv",
    index=False
)

print("\nAnalytics results saved successfully.")