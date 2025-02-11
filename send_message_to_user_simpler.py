from confluent_kafka import Producer
from logging import getLogger
import json

logger = getLogger(__name__)


def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(
            f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}"
        )


if __name__ == "__main__":
    # Kafka Producer configuration
    conf = {
        "bootstrap.servers": "kafka:9092",  # Replace with your Kafka broker
        "security.protocol": "PLAINTEXT",  # Change to 'SSL' or 'SASL_SSL' if needed
        # 'sasl.mechanism': 'PLAIN',  # Uncomment if using SASL authentication
        # 'sasl.username': 'your_username',  # Replace with your username
        # 'sasl.password': 'your_password',  # Replace with your password
    }

    producer = Producer(conf)

    topic = "chat-messages"
    key = "user-1234"
    message = json.dumps(
        {"message": "Hello, World!啦啦啦哈哈哈😄🎉", "ennded": False},
        ensure_ascii=False,
    )

    # Publish message
    producer.produce(topic=topic, key=key, value=message, callback=delivery_report)
    producer.flush()  # Wait until all messages are delivered

    logger.info("Message publishing complete.")
