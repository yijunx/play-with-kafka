from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KAFKA_HOST: Optional[str] = "kafka"
    KAFKA_PORT: Optional[str] = "9092"
    KAFKA_TOPIC: Optional[str] = "chat-messages"


configurations = Settings()


if __name__ == "__main__":
    print(configurations)
