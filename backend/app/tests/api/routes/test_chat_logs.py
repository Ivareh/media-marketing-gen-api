from collections.abc import Awaitable, Callable

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import ChatLog
from app.core.schemas.chat_log import ChatLogCreate, ChatLogUpdate
from app.tests.api.api_test_base import APITestBase
from app.tests.utils import (
    create_random_chat_log,
    model_random_create_chat_log,
    model_random_update_chat_log,
)


@pytest.fixture(scope="module")
def route() -> str:
    return "chat_logs"


@pytest_asyncio.fixture(scope="module")
async def obj_model_create() -> Callable[[AsyncSession], Awaitable[ChatLogCreate]]:
    async def random_create_chat_log(
        db: AsyncSession,
    ) -> ChatLogCreate:
        return await model_random_create_chat_log(db)

    return random_create_chat_log


@pytest_asyncio.fixture(scope="module")
async def obj_model_update() -> Callable[[AsyncSession], Awaitable[ChatLogUpdate]]:
    async def random_update_chat_log(
        db: AsyncSession,
    ) -> ChatLogUpdate:
        return await model_random_update_chat_log(db)

    return random_update_chat_log


@pytest_asyncio.fixture(scope="module")
async def obj_create() -> Callable[[AsyncSession], Awaitable[ChatLog]]:
    async def random_chat_log(
        db: AsyncSession,
    ) -> ChatLog:
        return await create_random_chat_log(db)

    return random_chat_log


class TestAPIChatLogs(APITestBase):
    skip_test_update = True
