from kafka import KafkaConsumer
import psycopg2
import json

# Connect to PostgreSQL
db = psycopg2.connect(
    host="localhost",
    port=5432,
    database="delivery_db",
    user="delivery_user",
    password="delivery_password"
)

cursor = db.cursor()

# Connect to Kafka
consumer = KafkaConsumer(
    "delivery_orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Waiting for orders...")

for message in consumer:

    order = message.value

    print("Received:", order)

    cursor.execute(
    """
    INSERT INTO orders (
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        customer_city,
        customer_state
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (order_id) DO UPDATE SET
        customer_city = EXCLUDED.customer_city,
        customer_state = EXCLUDED.customer_state
    """,
    (
        order["order_id"],
        order["customer_id"],
        order["order_status"],
        order["order_purchase_timestamp"],
        order["order_approved_at"],
        order["customer_city"],
        order["customer_state"]
    )
)
    db.commit()

    print("Saved to PostgreSQL:", order["order_id"])