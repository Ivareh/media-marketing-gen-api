import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import engine
from app.core.init_db import init_db
from app.logs.logger import logger, setup_logging


async def init() -> None:
    async with AsyncSession(engine) as db:
        await init_db(db)


async def main() -> None:
    setup_logging()
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
