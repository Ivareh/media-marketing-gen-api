from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Tenant
from app.core.schemas import TenantCreate, TenantUpdate
from app.crud import CRUD_tenants
from app.logs.logger import logger_test
from app.tests.utils.utils import random_lower_string, random_uuid


async def model_random_create_tenant(
    db: AsyncSession,  # noqa: ARG001
) -> TenantCreate:
    company_name = random_lower_string()
    entra_tenant_id = str(random_uuid())

    return TenantCreate(company_name=company_name, entra_tenant_id=entra_tenant_id)


async def model_random_update_tenant(
    db: AsyncSession,
) -> TenantUpdate:
    # Schemas for update is same as create
    tenant_create = await model_random_create_tenant(db)
    tenant_create = tenant_create.model_dump()
    return TenantUpdate(**tenant_create)


async def create_random_tenant(
    db: AsyncSession,
) -> Tenant:
    tenant_in = await model_random_create_tenant(db)
    tenant = await CRUD_tenants.create(db=db, obj_in=tenant_in)
    logger_test.error(tenant)
    return tenant[0]
