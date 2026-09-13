import pandas as pd

# Load orders dataset
df = pd.read_csv(
    "data/raw/olist_orders_dataset.csv",
    parse_dates=[
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
)

# Keep only orders that have an actual delivery date
delivered_orders = df.dropna(
    subset=["order_delivered_customer_date"]
).copy()

# Create late-delivery label
delivered_orders["is_late"] = (
    delivered_orders["order_delivered_customer_date"]
    > delivered_orders["order_estimated_delivery_date"]
).astype(int)

print(delivered_orders[
    [
        "order_id",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
        "is_late"
    ]
].head(10))

print("\nLate delivery counts:")
print(delivered_orders["is_late"].value_counts())

print("\nLate delivery percentage:")
print(
    delivered_orders["is_late"].mean() * 100
)

delivered_orders.to_csv(
    "data/processed/delivered_orders.csv",
    index=False
)

print("\nProcessed file saved successfully.")