import json
from logging import getLogger

from confluent_kafka import Producer

from app.config import configurations

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
        "bootstrap.servers": f"{configurations.KAFKA_HOST}:{configurations.KAFKA_PORT}",  # Replace with your Kafka broker
        "security.protocol": "PLAINTEXT",  # Change to 'SSL' or 'SASL_SSL' if needed
        # 'sasl.mechanism': 'PLAIN',  # Uncomment if using SASL authentication
        # 'sasl.username': 'your_username',  # Replace with your username
        # 'sasl.password': 'your_password',  # Replace with your password
    }

    producer = Producer(conf)

    topic = configurations.KAFKA_TOPIC
    key = "user-1234"
    message = json.dumps(
        {"message": "Hello, World!啦啦啦哈哈哈😄🎉", "ennded": False},
        ensure_ascii=False,
    )

    # Publish message
    producer.produce(topic=topic, key=key, value=message, callback=delivery_report)
    producer.flush(timeout=5)  # Wait until all messages are delivered

    logger.info("Message publishing complete.")
