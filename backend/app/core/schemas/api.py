from pydantic import BaseModel, Field


class FilterParams(BaseModel):
    limit: int | None = Field(None, gt=0)
    offset: int = Field(0, ge=0)
    sort_columns: list[str] | None = Field(None)
    sort_orders: list[str] | None = Field(None)


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: str | None = None


# Generic message
class Message(BaseModel):
    message: str
