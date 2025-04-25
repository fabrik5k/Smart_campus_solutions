from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["172.17.0.1:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_sensor_data(topic, data):
    producer.send(topic, value=data)
    producer.flush()
