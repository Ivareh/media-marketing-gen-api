from collections.abc import Awaitable, Callable

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Tenant
from app.core.schemas.tenant import TenantCreate, TenantUpdate
from app.crud import CRUD_tenants, CRUDBase
from app.tests.crud.crud_test_base import CRUDTestBase
from app.tests.utils import (
    create_random_tenant,
    model_random_create_tenant,
    model_random_update_tenant,
)


@pytest.fixture(scope="module")
def crud() -> CRUDBase:
    return CRUD_tenants


@pytest_asyncio.fixture(scope="module")
async def obj_model_create() -> Callable[[AsyncSession], Awaitable[TenantCreate]]:
    async def random_create_tenant(
        db: AsyncSession,
    ) -> TenantCreate:
        return await model_random_create_tenant(db)

    return random_create_tenant


@pytest_asyncio.fixture(scope="module")
async def obj_model_update() -> Callable[[AsyncSession], Awaitable[TenantUpdate]]:
    async def random_update_tenant(
        db: AsyncSession,
    ) -> TenantUpdate:
        return await model_random_update_tenant(db)

    return random_update_tenant


@pytest_asyncio.fixture(scope="module")
async def obj_create() -> Callable[[AsyncSession], Awaitable[Tenant]]:
    async def random_tenant(
        db: AsyncSession,
    ) -> Tenant:
        return await create_random_tenant(db)

    return random_tenant


class TestCRUDTenants(CRUDTestBase):
    num_initial_objs = 1
