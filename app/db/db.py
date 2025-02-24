from prisma import Prisma

prisma = Prisma()

async def db_connect():
    await prisma.connect()

async def db_disconnect():
    await prisma.disconnect()