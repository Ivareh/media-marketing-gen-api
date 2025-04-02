from typing import Annotated

from pydantic import BaseModel, ConfigDict, PlainValidator
from uuid import UUID

from app.core.schemas.field_validators import datetime_hour_utc_offset


# Shared session props
class _BaseChatSession(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    tenant_id: UUID


# Properties to receive on creation
class ChatSessionCreate(_BaseChatSession):
    pass


# Properties to receive on update
class ChatSessionUpdate(_BaseChatSession):
    pass


# Properties shared by models stored in DB
class _ChatSessionInDbBase(_BaseChatSession):
    id: UUID
    created_at: Annotated[str | None, PlainValidator(datetime_hour_utc_offset)]


# Properties to return to client
class ChatSessionPublic(_ChatSessionInDbBase):
    pass


# Properties stored in DB
class ChatSessionInDb(_ChatSessionInDbBase):
    pass
