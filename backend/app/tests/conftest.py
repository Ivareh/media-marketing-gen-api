from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.api.deps import get_db
from app.core.db import Base
from app.core.init_db import init_db
from app.main import app
from app.tests.test_db import test_engine
from app.tests.utils.utils import get_superuser_token_headers


@pytest_asyncio.fixture(scope="function")
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Uses CRUD_user, therefore AsyncSession
    async with AsyncSession(test_engine) as db:
        await init_db(db)

    yield test_engine

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def db(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    session = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        autobegin=False,
        expire_on_commit=False,
        bind=db_engine,
    )

    # NB: Needs to .begin() elsewhere
    async with session() as db:
        yield db

        await db.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest_asyncio.fixture(scope="function")
async def superuser_token_headers() -> dict[str, str]:
    return await get_superuser_token_headers()
