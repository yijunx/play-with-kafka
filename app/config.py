from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: Optional[str] = "redis"
    REDIS_PORT: Optional[str] = "6379"
    REDIS_USERNAME: Optional[str] = "default"
    REDIS_PASSWORD: Optional[str] = "passwordcool"


configurations = Settings()


if __name__ == "__main__":
    print(configurations)
