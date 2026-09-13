import pandas as pd

# Load processed orders
orders = pd.read_csv(
    "data/processed/delivered_orders.csv"
)

# Load customer data
customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

# Join orders with customers using customer_id
merged_data = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

# Display useful columns
print(
    merged_data[
        [
            "order_id",
            "customer_city",
            "customer_state",
            "is_late"
        ]
    ].head(10)
)

print("\nTotal rows:", len(merged_data))

print("\nMissing customer states:")
print(merged_data["customer_state"].isna().sum())

# Calculate late delivery percentage by state
state_summary = (
    merged_data
    .groupby("customer_state")
    .agg(
        total_orders=("order_id", "count"),
        late_orders=("is_late", "sum"),
        late_percentage=("is_late", "mean")
    )
    .reset_index()
)

state_summary["late_percentage"] = (
    state_summary["late_percentage"] * 100
)

state_summary = state_summary.sort_values(
    by="late_percentage",
    ascending=False
)

print("\nLate delivery by customer state:")
print(state_summary.head(10))