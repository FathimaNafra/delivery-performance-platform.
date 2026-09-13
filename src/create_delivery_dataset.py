import pandas as pd
import csv

# 1. Load datasets
orders = pd.read_csv(
    "data/processed/delivered_orders.csv"
)

customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

order_items = pd.read_csv(
    "data/raw/olist_order_items_dataset.csv"
)

sellers = pd.read_csv(
    "data/raw/olist_sellers_dataset.csv"
)


# 2. Add customer location
delivery_data = orders.merge(
    customers[
        [
            "customer_id",
            "customer_city",
            "customer_state"
        ]
    ],
    on="customer_id",
    how="left"
)


# 3. Keep one order-seller combination
order_sellers = order_items[
    [
        "order_id",
        "seller_id"
    ]
].drop_duplicates()


# 4. Add seller to orders
delivery_data = delivery_data.merge(
    order_sellers,
    on="order_id",
    how="left"
)


# 5. Add seller location
delivery_data = delivery_data.merge(
    sellers[
        [
            "seller_id",
            "seller_city",
            "seller_state"
        ]
    ],
    on="seller_id",
    how="left"
)


# 6. Show result
print("\nMain Delivery Dataset")
print("---------------------")

print(delivery_data[
    [
        "order_id",
        "customer_state",
        "seller_state",
        "is_late"
    ]
].head(10))

print("\nTotal rows:", len(delivery_data))


# 7. Save dataset
delivery_data.to_csv(
    "data/processed/delivery_dataset.csv",
    index=False,
    quoting=csv.QUOTE_ALL,
    quotechar='"'
)

print("\nSaved: data/processed/delivery_dataset.csv")