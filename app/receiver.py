import logging
import time

from confluent_kafka import Consumer
from flask_sock import Server

from app.config import configurations

logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")
import uuid


class Receiver:

    def __init__(
        self,
        routing_key: str,
    ):
        # later we use the configuration haha
        conf = {
            "bootstrap.servers": f"{configurations.KAFKA_HOST}:{configurations.KAFKA_PORT}",
            # all browser tabs get the lastest message only
            "group.id": str(uuid.uuid4()),
            "auto.offset.reset": "latest",
            # one browser, but gets all message from earliest once
            # cos the auto.commit is True
            # "group.id": "fixed-froup-how",
            # "auto.offset.reset": "earliest",
            # 'enable.auto.commit': True,
        }

        self.consumer = Consumer(conf)
        # here we can do multiple topic
        self.consumer.subscribe([configurations.KAFKA_TOPIC])
        self.routing_key = routing_key

    def start(self, ws: Server):
        logger.debug(f"Start receiving messages for {self.routing_key}")
        try:
            while True:
                msg = self.consumer.poll(1.0)
                if ws.connected is False:
                    self.terminate()
                    print("Connection closed")
                    break

                if msg is None:
                    # print("No message received")
                    continue
                print("### message ###")
                print(msg.key())
                print(msg.value().decode("utf-8"))
                print("### message ###")
                if msg.key() and msg.key().decode("utf-8") == self.routing_key:
                    ws.send(msg.value().decode("utf-8"))

        except Exception as e:
            logger.debug(e)
            self.terminate()

    def terminate(self):
        try:
            self.consumer.close()
            logger.debug(f"Session ended. Queue for {self.routing_key} is cleared")
        except Exception as e:
            logger.error(f"Connection close error: {e}")
