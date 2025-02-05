# # # gunicorn -b 0.0.0.0:5000 --workers 4 --threads 100 app.main:app

import json
import logging
import re

import jwt
from flask import Flask, request
from flask_cors import CORS
from flask_sock import Server, Sock

from app.receiver import Receiver

logger = logging.getLogger(__name__)

logger.addHandler(logging.StreamHandler())
logger.setLevel("DEBUG")

app = Flask(__name__)
app.config["SOCK_SERVER_OPTIONS"] = {"ping_interval": 25}
cors = CORS(app)
sock = Sock(app)


# class User(BaseModel):
#     name: str
#     id: str


# def get_actor_from_request(request: Request) -> User:
#     token = request.args.get("user_id")
#     logger.warning(token)
#     payload = jwt.decode(token, options={"verify_signature": False})
#     logger.warning(payload)
#     try:
#         actor = User(
#             name=payload["name"],
#             id=payload["sub"]
#         )
#     except Exception:
#         logger.warning("failed to create actor from internal token")
#     return actor


@app.route("/internal/liveness", methods=["GET"])
def liveness():
    return {"hello": "i am alive"}


@sock.route("/user-notification/v1/generic-connect")
def connect(ws: Server):
    # used the auth to check if user_id and chat_id are replated
    user_id = request.args.get("user_id")
    chat_id = request.args.get("chat_id")
    try:
        # actor = get_actor_from_request(request)
        logger.info(f"authenticated user: {user_id}")
        # delete below line
        # pass
        ws.send(json.dumps({"content": "websocket connected!", "type": "muttering"}))
    except Exception as e:
        logger.error(f"authenticate error {e}")
        ws.send(json.dumps({"message": e}))
        return

    try:
        # lets separate the routing key for eve
        r = Receiver(routing_key=chat_id)
        r.start(ws)
    except Exception as e:
        logger.error(f"receiver error {e}")
        ws.send({"error": e})
        return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
