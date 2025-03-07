from redis.asyncio import Redis
from app.core.logger import logger
from fastapi_limiter import FastAPILimiter


async def init_limiter(redis: Redis):
    if not redis:
        logger.error("Redis must be initialized before limiter")
        return
    await FastAPILimiter.init(redis)
    logger.info("✅ RateLimiter initialized successfully")


async def close_limiter():
    await FastAPILimiter.close()
    logger.info("❌ RateLimiter closed successfully")
