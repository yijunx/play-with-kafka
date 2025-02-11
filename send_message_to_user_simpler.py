# import redis
# from logging import getLogger
# import json


# logger = getLogger(__name__)

# if __name__ == "__main__":
#     r = redis.Redis(
#         host="redis.middleware.dev.motiong.net",
#         port="6379",
#         username="default",
#         password="i dont want to tell you",
#     )
#     routing_key = "user-id"
#     r.publish(routing_key, json.dumps({"message": "Hello, World!", "ennded": False}))
#     r.close()


from confluent_kafka import Producer
from logging import getLogger
import json

logger = getLogger(__name__)

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

if __name__ == "__main__":
    # Kafka Producer configuration
    conf = {
        'bootstrap.servers': 'kafka:9092',  # Replace with your Kafka broker
        'security.protocol': 'PLAINTEXT',  # Change to 'SSL' or 'SASL_SSL' if needed
        # 'sasl.mechanism': 'PLAIN',  # Uncomment if using SASL authentication
        # 'sasl.username': 'your_username',  # Replace with your username
        # 'sasl.password': 'your_password',  # Replace with your password
    }

    producer = Producer(conf)
    
    topic = "chat-messages"
    key="user-1234"
    message = json.dumps({"message": "Hello, World!", "ennded": False})

    # Publish message
    producer.produce(topic=topic, key=key, value=message, callback=delivery_report)
    producer.flush()  # Wait until all messages are delivered

    logger.info("Message publishing complete.")
