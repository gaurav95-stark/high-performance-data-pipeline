import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    worker_count: int = int(os.getenv("WORKER_COUNT", "4"))
    queue_max_size: int = int(os.getenv("QUEUE_MAX_SIZE", "1000"))
    database_path: str = os.getenv("DATABASE_PATH", "./data/pipeline.db")
    cache_ttl_seconds: int = int(os.getenv("CACHE_TTL_SECONDS", "30"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
