from kafka import KafkaProducer
import json
import time

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

# Adjust the bootstrap_servers based on your environment:
# For host-based access, use 'localhost:9092'; for intra-Docker communication, use 'kafka:9092'
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=json_serializer
)

topic = "test-topic"

if __name__ == '__main__':
    for i in range(10):
        message = {"number": i}
        producer.send(topic, message)
        print(f"Sent: {message}")
        time.sleep(1)
    
    # Ensure all messages are sent before closing the producer
    producer.flush()