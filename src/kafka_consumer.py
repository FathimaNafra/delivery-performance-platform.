from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "delivery_orders",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Waiting for orders...")

for message in consumer:
    order = message.value
    print("Received:", order)