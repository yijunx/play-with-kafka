import logging
import time

import redis
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

        self.r = redis.Redis(
            host=configurations.REDIS_HOST,
            port=configurations.REDIS_PORT,
            username=configurations.REDIS_USERNAME,
            password=configurations.REDIS_PASSWORD,
        )
        self.routing_key = routing_key
        self.p = self.r.pubsub()
        self.p.subscribe(self.routing_key)

    def start(self, ws: Server):
        logger.debug(f"Start receiving messages for {self.routing_key}")
        try:
            while True:
                message = self.p.get_message()
                if message and message["type"] == "message":
                    string_data = message["data"].decode("utf-8")
                    ws.send(string_data)
                time.sleep(0.01)

                if ws.connected is False:
                    self.terminate()
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


if __name__ == "__main__":
    r = Receiver(routing_key="user-id")

    def callback(body):
        print(body.decode("utf-8"))
        # try json..

    r.start(callback=callback)
