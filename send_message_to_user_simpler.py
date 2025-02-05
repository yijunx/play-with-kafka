import redis
from logging import getLogger
import json


logger = getLogger(__name__)

if __name__ == "__main__":
    r = redis.Redis(
        host="redis.middleware.dev.motiong.net",
        port="6379",
        username="default",
        password="i dont want to tell you",
    )
    routing_key = "user-id"
    r.publish(routing_key, json.dumps({"message": "Hello, World!", "ennded": False}))
    r.close()
