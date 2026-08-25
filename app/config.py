from pydantic_settings import BaseSettings
from functools import lru_cache

class settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    TIME_EXPIRED: int
    ALGORITHM: str
    APP_NAME: str = "VlogTravels"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

@lru_cache
def get_settings() -> settings:
    return settings()
