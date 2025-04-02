from qdrant_client import AsyncQdrantClient
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

qdrant_client = AsyncQdrantClient(url=str(settings.QDRANT_URL))

engine = create_async_engine(str(settings.OLTP_DATABASE_URI))

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
    autobegin=False,
)


class Base(AsyncAttrs, DeclarativeBase):
    pass
