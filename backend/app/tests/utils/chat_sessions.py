from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import ChatSession, Tenant, User
from app.core.schemas import ChatSessionCreate, ChatSessionUpdate
from app.crud import CRUD_chat_sessions
from app.tests.utils.tenants import create_random_tenant
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import ModelDeps, create_dep_ids_map


class ChatSessionDeps(ModelDeps):
    tenant: Tenant
    user: User


async def _create_chat_session_deps(db: AsyncSession) -> ChatSessionDeps:
    tenant = await create_random_tenant(db)
    user = await create_random_user(db)
    deps: ChatSessionDeps = {"tenant": tenant, "user": user}
    return deps


async def model_random_create_chat_session(
    db: AsyncSession,
    deps: ChatSessionDeps | None = None,
) -> ChatSessionCreate:
    """If input deps, all dependencies for chat session must be provided"""
    # Prepare deps
    if deps is None:
        deps = await _create_chat_session_deps(db)
    dep_ids_map = create_dep_ids_map(deps, ChatSessionDeps)

    # Model create session
    user_id = dep_ids_map["user"]
    tenant_id = dep_ids_map["tenant"]
    return ChatSessionCreate(user_id=user_id, tenant_id=tenant_id)


async def model_random_update_chat_session(
    db: AsyncSession,
    deps: ChatSessionDeps | None = None,
) -> ChatSessionUpdate:
    # Schemas for update is same as create
    chat_session_create = await model_random_create_chat_session(db, deps)
    chat_session_create = chat_session_create.model_dump()
    return ChatSessionUpdate(**chat_session_create)


async def create_random_chat_session(
    db: AsyncSession,
    deps: ChatSessionDeps | None = None,
) -> ChatSession:
    chat_session_in = await model_random_create_chat_session(db, deps)

    chat_session = await CRUD_chat_sessions.create(db=db, obj_in=chat_session_in)
    return chat_session[0]
