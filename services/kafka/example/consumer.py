import sys
import json
from kafka import KafkaConsumer


def main(topic: str, kafka_host: str):
    if (topic is None):
        print("Topic can't be NULL/None")
    else:
        print(f"Consumer - Kafka: '{kafka_host}' - Topic: '{topic}'")

        consumer = KafkaConsumer(
            topic,
            value_deserializer = __value_deserializer,
            bootstrap_servers = kafka_host
        )
        for msg in consumer:
            print(msg.value)

def __value_deserializer(data: bytes):
    return json.loads(data.decode("utf-8"))


if __name__ == "__main__":
    _, topic, kafka_host, *_ = (*sys.argv, *[None for _ in range(2)])
    params = {
        "topic": topic,
        "kafka_host": kafka_host if (kafka_host) else "localhost:29200"
    }
    main(**params)