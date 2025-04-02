from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from app.core.config import settings
from app.core.models import Tenant, User
from app.core.schemas import UserCreate
from app.core.schemas.tenant import TenantCreate
from app.logs.logger import logger


async def init_db(db: AsyncSession) -> None:
    logger.info("Checking if first superuser objects exists")
    async with db.begin():
        # Check if first tenant exists
        tenant = await db.execute(
            select(Tenant).where(
                Tenant.entra_tenant_id == settings.FIRST_SUPERUSER_TENANT_ID
            )
        )
        tenant = tenant.scalar()
        if not tenant:
            logger.info("Creating first superuser's tenant")
            tenant_in = TenantCreate(
                company_name="Media Market API Company",
                entra_tenant_id=settings.FIRST_SUPERUSER_TENANT_ID,
            )
            tenant_data = tenant_in.model_dump()
            tenant = Tenant(**tenant_data)
            db.add(tenant)
            logger.info("Successfully created first tenant")

        # Check if first user exists
        user = await db.execute(
            select(User).where(User.email == settings.FIRST_SUPERUSER_EMAIL)
        )
        user = user.scalar()
        if not user:
            tenant_id = await tenant.awaitable_attrs.id
            logger.info("Creating first superuser")
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                entra_id=settings.FIRST_SUPERUSER_ENTRA_ID,
                tenant_id=str(tenant_id),
                role="admin",
                full_name=None,
            )
            user_data = user_in.model_dump()
            user = User(**user_data)
            db.add(user)
            logger.info("Successfully created first superuser")
        await db.flush()
