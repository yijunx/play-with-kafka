import logging
import time

from confluent_kafka import Consumer
from flask_sock import Server

from app.config import configurations

logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")


class Receiver:

    def __init__(
        self,
        routing_key: str,
    ):
        # later we use the configuration haha
        conf = {
            "bootstrap.servers": "kafka:9092",
            "group.id": "frontend-user-1234",
            "auto.offset.reset": "earliest",
        }

        self.consumer = Consumer(conf)
        self.consumer.subscribe(["chat-messages"])
        self.routing_key = routing_key

    def start(self, ws: Server):
        logger.debug(f"Start receiving messages for {self.routing_key}")
        try:
            while True:
                # message = self.p.get_message()
                # if message and message["type"] == "message":
                #     string_data = message["data"].decode("utf-8")
                #     ws.send(string_data)
                # time.sleep(0.01)
                msg = self.consumer.poll(1.0)
                if msg is None:
                    # print("No message received")
                    continue
                print(msg.key())
                print(msg.key().decode("utf-8"))
                if msg.key().decode("utf-8") == self.routing_key:
                    ws.send(msg.value().decode("utf-8"))

                if ws.connected is False:
                    self.terminate()
                    print("Connection closed")
                    break
        except Exception as e:
            logger.debug(e)
            self.terminate()

    def terminate(self):
        try:
            self.r.close()
            logger.debug(f"Session ended. Queue for {self.routing_key} is cleared")
        except Exception as e:
            logger.error(f"Connection close error: {e}")


# if __name__ == "__main__":
#     r = Receiver(routing_key="user-id")

#     def callback(body):
#         print(body.decode("utf-8"))
#         # try json..

#     r.start(callback=callback)
