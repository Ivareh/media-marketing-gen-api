from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    get_db,
)
from app.api.message_utils import (
    delete_return_msg,
)
from app.core.schemas import (
    FilterParams,
    TenantCreate,
    TenantPublic,
    TenantUpdate,
)
from app.crud import CRUD_tenants

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get(
    "/{tenant_id}",
    response_model=TenantPublic,
)
async def get_tenant(
    tenant_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Get tenant by value for `tenant_id`.

    Returns the tenant.
    """

    tenant_map = {"id": tenant_id}
    tenant = await CRUD_tenants.get(db=db, filters=tenant_map)

    return tenant[0]


@router.get(
    "/",
    response_model=list[TenantPublic],
)
async def get_all_tenants(
    filter_params: Annotated[FilterParams, Query()],
    db: AsyncSession = Depends(get_db),
):
    """
    Get all tenants.

    Returns a list of all tenants.
    """

    all_tenants = await CRUD_tenants.get_all(db=db, filter_params=filter_params)

    return all_tenants


@router.post(
    "/",
    response_model=list[TenantPublic] | None,
)
async def create_tenant(
    tenants: TenantCreate | list[TenantCreate],
    return_nothing: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a list of tenants.

    Returns the list of tenants.
    """
    created_tenants = await CRUD_tenants.create(
        db=db, obj_in=tenants, return_nothing=return_nothing
    )

    return created_tenants


@router.patch(
    "/{tenant_id}",
    response_model=TenantPublic,
)
async def update_tenant(
    tenant_id: UUID4,
    tenant_update: TenantUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a tenant for `tenant_id`.

    Returns the updated tenant
    """
    updated_tenant = await CRUD_tenants.update(
        db=db, obj_id=tenant_id, obj_in=tenant_update
    )

    updated_tenant_public = TenantPublic.model_validate(updated_tenant)

    return updated_tenant_public


@router.delete(
    "/{tenant_id}",
    response_model=str,
)
async def delete_tenant(
    tenant_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a tenant for `tenant_id`.

    Returns a message indicating the tenant was deleted.
    """

    tenant_map = {"id": tenant_id}
    await CRUD_tenants.delete(db=db, filters=tenant_map)

    return delete_return_msg(objs="Tenant", filters=tenant_map).message
