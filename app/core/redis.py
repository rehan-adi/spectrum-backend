from app.core.logger import logger
from app.core.config import settings
from redis.asyncio import Redis, ConnectionPool

redis: Redis | None = None


async def connect_redis():
    global redis
    try:
        pool = ConnectionPool.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)  # type: ignore
        redis = Redis(connection_pool=pool)
        logger.info("✅ Redis connected successfully")
    except Exception as e:
        logger.error(f"❌ Redis connection failed: {e}")
        raise


async def disconnect_redis():
    if redis:
        await redis.close()
        logger.info("✅ Redis connection closed")
