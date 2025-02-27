from prisma import Prisma
from app.core.logger import logger

prisma = Prisma()


async def db_connect():
    try:
        await prisma.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")


async def db_disconnect():
    try:
        await prisma.disconnect()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Database disconnection failed: {e}")
