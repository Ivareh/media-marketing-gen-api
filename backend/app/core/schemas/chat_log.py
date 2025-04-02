from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, PlainValidator

from app.core.schemas.field_validators import datetime_hour_utc_offset


# Shared session props
class _BaseChatLog(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    chat_session_id: UUID
    prompt: str
    response_text: str


# Properties to receive on creation
class ChatLogCreate(_BaseChatLog):
    pass


# Properties to receive on update
class ChatLogUpdate(_BaseChatLog):
    pass


# Properties shared by models stored in DB
class _ChatLogInDbBase(_BaseChatLog):
    id: UUID
    created_at: Annotated[str | None, PlainValidator(datetime_hour_utc_offset)]


# Properties to return to client
class ChatLogPublic(_ChatLogInDbBase):
    pass


# Properties stored in DB
class ChatLogInDb(_ChatLogInDbBase):
    pass
