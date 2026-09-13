import pandas as pd

# Load processed orders
orders = pd.read_csv(
    "data/processed/delivered_orders.csv"
)

# Load order items
order_items = pd.read_csv(
    "data/raw/olist_order_items_dataset.csv"
)

# Load seller data
sellers = pd.read_csv(
    "data/raw/olist_sellers_dataset.csv"
)

# Join orders with order items
order_seller = orders.merge(
    order_items[
        [
            "order_id",
            "seller_id"
        ]
    ],
    on="order_id",
    how="left"
)

# Join seller information
order_seller = order_seller.merge(
    sellers,
    on="seller_id",
    how="left"
)

print(
    order_seller[
        [
            "order_id",
            "seller_id",
            "seller_city",
            "seller_state",
            "is_late"
        ]
    ].head(10)
)

print("\nTotal rows:", len(order_seller))

print("\nMissing seller states:")
print(order_seller["seller_state"].isna().sum())

# Remove duplicate order-seller combinations
seller_orders = order_seller[
    [
        "order_id",
        "seller_id",
        "seller_city",
        "seller_state",
        "is_late"
    ]
].drop_duplicates()

# Calculate seller performance
seller_summary = (
    seller_orders
    .groupby(
        [
            "seller_id",
            "seller_city",
            "seller_state"
        ]
    )
    .agg(
        total_orders=("order_id", "count"),
        late_orders=("is_late", "sum"),
        late_percentage=("is_late", "mean")
    )
    .reset_index()
)

seller_summary["late_percentage"] = (
    seller_summary["late_percentage"] * 100
)

# Keep sellers with at least 20 orders
seller_summary = seller_summary[
    seller_summary["total_orders"] >= 20
]

# Sort by highest late percentage
seller_summary = seller_summary.sort_values(
    by="late_percentage",
    ascending=False
)

print("\nSeller delivery performance:")
print(seller_summary.head(10))