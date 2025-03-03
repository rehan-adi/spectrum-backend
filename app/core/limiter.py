from app.core.redis import redis
from fastapi_limiter import FastAPILimiter


async def init_limiter():
    if not redis:
        raise ValueError("Redis must be initialized before limiter")
    await FastAPILimiter.init(redis)  # type: ignore


async def close_limiter():
    await FastAPILimiter.close()
