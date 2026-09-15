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

# Take only 5 orders for testing
df = df.head(100)

# Send each order to Kafka
for _, row in df.iterrows():

    order = {
        "order_id": row["order_id"],
        "customer_id": row["customer_id"],
        "order_status": row["order_status"],
        "order_purchase_timestamp": row["order_purchase_timestamp"],
        "order_approved_at": row["order_approved_at"]
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