from typing import Annotated

from uuid import UUID
from pydantic import (
    PlainValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

from app.core.schemas.field_validators import datetime_hour_utc_offset


# Shared properties
class _BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field(max_length=255)
    full_name: str | None = Field(max_length=70)
    role: str = Field(max_length=30, default="guest")
    settings: dict[str, str] | None = None


# Properties to receive via API on creation
class UserCreate(_BaseUser):
    entra_id: str
    tenant_id: UUID


# Properties to receive via API on update
class UserUpdate(_BaseUser):
    entra_id: str
    tenant_id: UUID


class UserUpdateSettings(BaseModel):
    settings: dict[str, str]


# Properties to return via API
class UserPublic(_BaseUser):
    id: UUID
    entra_id: str
    tenant_id: UUID
    created_at: Annotated[str, PlainValidator(datetime_hour_utc_offset)]
    updated_at: Annotated[str | None, PlainValidator(datetime_hour_utc_offset)]


# Properties on multiple users
class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


class _UserInDbBase(_BaseUser):
    id: UUID
    entra_id: str
    tenant_id: UUID
    created_at: Annotated[str, PlainValidator(datetime_hour_utc_offset)]
    updated_at: Annotated[str, PlainValidator(datetime_hour_utc_offset)]


class UserInDb(_UserInDbBase):
    pass
