from app.core.models import ChatLog, ChatSession, Tenant, User
from app.core.schemas import (
    ChatLogCreate,
    ChatLogPublic,
    ChatLogUpdate,
    ChatSessionCreate,
    ChatSessionPublic,
    ChatSessionUpdate,
    TenantCreate,
    TenantPublic,
    TenantUpdate,
    UserCreate,
    UserPublic,
    UserUpdate,
)
from app.crud.base import CRUDBase

CRUD_tenants = CRUDBase[
    Tenant,
    TenantPublic,
    TenantCreate,
    TenantUpdate,
](
    model=Tenant,
    schema=TenantPublic,
    create_schema=TenantCreate,
)


CRUD_chat_sessions = CRUDBase[
    ChatSession,
    ChatSessionPublic,
    ChatSessionCreate,
    ChatSessionUpdate,
](
    model=ChatSession,
    schema=ChatSessionPublic,
    create_schema=ChatSessionCreate,
)

CRUD_chat_logs = CRUDBase[
    ChatLog,
    ChatLogPublic,
    ChatLogCreate,
    ChatLogUpdate,
](
    model=ChatLog,
    schema=ChatLogPublic,
    create_schema=ChatLogCreate,
)


CRUD_users = CRUDBase[
    User,
    UserPublic,
    UserCreate,
    UserUpdate,
](
    model=User,
    schema=UserPublic,
    create_schema=UserCreate,
)
