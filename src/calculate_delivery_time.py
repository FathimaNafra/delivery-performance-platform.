import pandas as pd

# Load main delivery dataset
df = pd.read_csv(
    "data/processed/delivery_dataset.csv",
    parse_dates=[
        "order_purchase_timestamp",
        "order_delivered_customer_date"
    ]
)

# Calculate delivery time in days
df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.days

print(
    df[
        [
            "order_id",
            "order_purchase_timestamp",
            "order_delivered_customer_date",
            "delivery_days"
        ]
    ].head(10)
)

print("\nAverage delivery time:")
print(df["delivery_days"].mean())

# Average delivery time by customer state
state_delivery = (
    df.groupby("customer_state")
    .agg(
        total_orders=("order_id", "count"),
        average_delivery_days=("delivery_days", "mean")
    )
    .reset_index()
)

state_delivery = state_delivery.sort_values(
    by="average_delivery_days",
    ascending=False
)

print("\nStates with longest average delivery time:")
print(state_delivery.head(10))

# Remove duplicate order-seller combinations
seller_delivery_data = df[
    [
        "order_id",
        "seller_id",
        "seller_city",
        "seller_state",
        "delivery_days"
    ]
].drop_duplicates()

# Calculate average delivery time for each seller
seller_delivery = (
    seller_delivery_data
    .groupby(
        [
            "seller_id",
            "seller_city",
            "seller_state"
        ]
    )
    .agg(
        total_orders=("order_id", "count"),
        average_delivery_days=("delivery_days", "mean")
    )
    .reset_index()
)

# Keep sellers with at least 20 orders
seller_delivery = seller_delivery[
    seller_delivery["total_orders"] >= 20
]

# Longest delivery time first
seller_delivery = seller_delivery.sort_values(
    by="average_delivery_days",
    ascending=False
)

print("\nSellers with longest average delivery time:")

print(
    seller_delivery[
        [
            "seller_city",
            "seller_state",
            "total_orders",
            "average_delivery_days"
        ]
    ].head(10)
)