import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    REDIS_URL = os.getenv("REDIS_URL")
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY") or "secret"
    
    ACCESS_TOKEN_EXPIRE_MINUTES = 2  # 2 days
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]


settings = Settings()
