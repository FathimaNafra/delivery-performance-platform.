from kafka import KafkaProducer
import pandas as pd
import json
import time

# Connect Python producer to Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# Read the real Olist orders dataset
df = pd.read_csv(
    "data/raw/olist_orders_dataset.csv"
)

# Read the Olist customers dataset
customers = pd.read_csv(
    "data/raw/olist_customers_dataset.csv"
)

order_items = pd.read_csv(
    "data/raw/olist_order_items_dataset.csv"
)

order_summary = order_items.groupby("order_id").agg(
    item_count=("order_item_id", "count"),
    total_price=("price", "sum"),
    total_freight=("freight_value", "sum")
).reset_index()
df = df.merge(
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

df = df.merge(
    order_summary,
    on="order_id",
    how="left"
)

# Take only 5 orders for testing
df = df.head(100)

# Send each order to Kafka
for _, row in df.iterrows():

    order = {
        "order_id": row["order_id"],
        "customer_id": row["customer_id"],
        "order_status": row["order_status"],
        "order_purchase_timestamp": row["order_purchase_timestamp"],
        "order_approved_at": row["order_approved_at"],
        "customer_city": row["customer_city"],
        "customer_state": row["customer_state"],
        "item_count": int(row["item_count"]),
        "total_price": float(row["total_price"]),
        "total_freight": float(row["total_freight"])
    }

    producer.send(
        "delivery_orders",
        value=order
    )

    print("Sent:", order)

    # Wait 2 seconds before sending the next order
    time.sleep(0.1)

producer.flush()
producer.close()

print("\nFinished sending 5 Olist orders.")