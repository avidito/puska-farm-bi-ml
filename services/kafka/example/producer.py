import sys
import json
from kafka import KafkaProducer


def main(kafka_host: str, topic: str, message: str):
    if (topic is None):
        print("Topic can't be NULL/None")
    elif (message is None):
        print("Message can't be NULL/None")
    else:
        print(f"Producer - Kafka: '{kafka_host}' - Topic: '{topic}'")
        
        producer = KafkaProducer(
            value_serializer = __value_serializer,
            bootstrap_servers = kafka_host
        )
        producer.send(topic, message)

def __value_serializer(data: dict):
    return json.dumps(data).encode("utf-8")


if __name__ == "__main__":
    # CONFIG
    kafka_host = "localhost:29200"
    topic = "produksi"
    message = {"message": "data"}

    main(kafka_host, topic, message)
