from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# Shared session props
class _BaseTenant(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    company_name: str
    entra_tenant_id: str
    settings: dict[str, Any] | None = None


# Properties to receive on creation
class TenantCreate(_BaseTenant):
    pass


# Properties to receive on update
class TenantUpdate(_BaseTenant):
    pass


# Properties shared by models stored in DB
class _TenantInDbBase(_BaseTenant):
    id: UUID


# Properties to return to client
class TenantPublic(_TenantInDbBase):
    pass


# Properties stored in DB
class TenantInDb(_TenantInDbBase):
    pass
