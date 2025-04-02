from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

# Parameter values from docker-compose.test.yml
TEST_OLTP_DATABASE_URI: PostgresDsn | None = MultiHostUrl.build(
    scheme="postgresql+asyncpg",
    username="postgres",
    password="test",
    host="test-db",
    port=5432,
    path="test-media-market-oltp-db",
)

test_engine = create_async_engine(
    str(TEST_OLTP_DATABASE_URI),
    poolclass=NullPool,
)
