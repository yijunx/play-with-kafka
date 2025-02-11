# play-with-kafka
kafka for streaming chat


## how to setup

reopen in devcontainer.


something worth notice is that, to have type hint for confluent kafka we need to:

```
poetry add --group dev types-confluent-kafka
```

cos the original confluent-kafka is written in C, thus no type hint. so we need the magic above. (just install can already)


## lesson learnt

there is some important configuration setup for consumer

### setup for multiple chat window, but only takes latest message

Ensure Each User Only Sees New Messages:

Use unique group.ids for different sessions (if needed).
Use auto.offset.reset='latest' to only get new messages.
```python
conf = {
    "bootstrap.servers": f"{configurations.KAFKA_HOST}:{configurations.KAFKA_PORT}",
    # all browser tabs get the lastest message only
    "group.id": str(uuid.uuid4()),
    "auto.offset.reset": "latest",
    # we dont need to turn it on
    # "enable.auto.commit": True,
    # cos now commit makes no sense, no way backend returns the group id
    # cos its uuid!!!
}
```

### setup for replay for a client from begining, but only once

Avoid Duplicate Messages:

Use a fixed group.id for persistent consumers (like a server).
Let browsers or frontend clients use ephemeral consumers if they only need live messages.

```python
conf = {
    "bootstrap.servers": f"{configurations.KAFKA_HOST}:{configurations.KAFKA_PORT}",
    "group.id": "replay-all-message-for-specific-test",
    "auto.offset.reset": "earliest",
    # now commit makes sense
    # cos we dont want to replay duplicated message!!
    "enable.auto.commit": True,
}
```


### Why Is Offset Commit at the Group Level?

ask chatgpt pls!