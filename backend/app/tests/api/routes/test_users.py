from collections.abc import Awaitable, Callable

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import User
from app.core.schemas.user import UserCreate, UserUpdate
from app.tests.api.api_test_base import APITestBase
from app.tests.utils import (
    create_random_user,
    model_random_create_user,
    model_random_update_user,
)


@pytest.fixture(scope="module")
def route() -> str:
    return "users"


@pytest_asyncio.fixture(scope="module")
async def obj_model_create() -> Callable[[AsyncSession], Awaitable[UserCreate]]:
    async def random_create_user(
        db: AsyncSession,
    ) -> UserCreate:
        return await model_random_create_user(db)

    return random_create_user


@pytest_asyncio.fixture(scope="module")
async def obj_model_update() -> Callable[[AsyncSession], Awaitable[UserUpdate]]:
    async def random_update_user(
        db: AsyncSession,
    ) -> UserUpdate:
        return await model_random_update_user(db)

    return random_update_user


@pytest_asyncio.fixture(scope="module")
async def obj_create() -> Callable[[AsyncSession], Awaitable[User]]:
    async def random_user(
        db: AsyncSession,
    ) -> User:
        return await create_random_user(db)

    return random_user


class TestAPIUsers(APITestBase):
    num_initial_objs = 1
