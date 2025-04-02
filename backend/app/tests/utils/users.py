from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Tenant, User
from app.core.schemas import UserCreate, UserUpdate
from app.crud import CRUD_users
from app.tests.utils.tenants import create_random_tenant
from app.tests.utils.utils import (
    ModelDeps,
    create_dep_ids_map,
    random_email,
    random_full_name,
    random_uuid,
)


class UserDeps(ModelDeps):
    tenant: Tenant


async def _create_user_deps(db: AsyncSession) -> UserDeps:
    tenant = await create_random_tenant(db)
    deps: UserDeps = {"tenant": tenant}
    return deps


async def model_random_create_user(
    db: AsyncSession, deps: UserDeps | None = None
) -> UserCreate:
    """If input deps, all dependencies for user must be provided"""
    # Prepare deps
    if deps is None:
        deps = await _create_user_deps(db)
    dep_ids_map = create_dep_ids_map(deps, UserDeps)

    # Model create user
    email = random_email()
    full_name = random_full_name()
    entra_id = str(random_uuid())
    tenant_id = dep_ids_map["tenant"]

    return UserCreate(
        email=email, full_name=full_name, entra_id=entra_id, tenant_id=tenant_id
    )


async def model_random_update_user(
    db: AsyncSession, deps: UserDeps | None = None
) -> UserUpdate:
    # Schemas for update is same as create
    user_create = await model_random_create_user(db, deps)
    user_create = user_create.model_dump()
    return UserUpdate(**user_create)


async def create_random_user(
    db: AsyncSession,
    deps: UserDeps | None = None,
) -> User:
    user_in = await model_random_create_user(db, deps)

    user = await CRUD_users.create(db=db, obj_in=user_in)
    return user[0]
