from collections.abc import Awaitable, Callable

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import ChatSession
from app.core.schemas.chat_session import ChatSessionCreate, ChatSessionUpdate
from app.crud import CRUD_chat_sessions, CRUDBase
from app.tests.crud.crud_test_base import CRUDTestBase
from app.tests.utils import (
    create_random_chat_session,
    model_random_create_chat_session,
    model_random_update_chat_session,
)


@pytest.fixture(scope="module")
def crud() -> CRUDBase:
    return CRUD_chat_sessions


@pytest_asyncio.fixture(scope="module")
async def obj_model_create() -> Callable[[AsyncSession], Awaitable[ChatSessionCreate]]:
    async def random_create_chat_session(
        db: AsyncSession,
    ) -> ChatSessionCreate:
        return await model_random_create_chat_session(db)

    return random_create_chat_session


@pytest_asyncio.fixture(scope="module")
async def obj_model_update() -> Callable[[AsyncSession], Awaitable[ChatSessionUpdate]]:
    async def random_update_chat_session(
        db: AsyncSession,
    ) -> ChatSessionUpdate:
        return await model_random_update_chat_session(db)

    return random_update_chat_session


@pytest_asyncio.fixture(scope="module")
async def obj_create() -> Callable[[AsyncSession], Awaitable[ChatSession]]:
    async def random_chat_session(
        db: AsyncSession,
    ) -> ChatSession:
        return await create_random_chat_session(db)

    return random_chat_session


class TestCRUDChatSessions(CRUDTestBase):
    pass
