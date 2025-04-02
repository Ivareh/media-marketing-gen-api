from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import ChatLog, ChatSession
from app.core.schemas import ChatLogCreate, ChatLogUpdate
from app.crud import CRUD_chat_logs
from app.tests.utils.chat_sessions import create_random_chat_session
from app.tests.utils.utils import (
    ModelDeps,
    create_dep_ids_map,
    random_lower_string,
)


class ChatLogDeps(ModelDeps):
    chat_session: ChatSession


async def _create_chat_log_deps(db: AsyncSession) -> ChatLogDeps:
    chat_session = await create_random_chat_session(db)
    deps: ChatLogDeps = {"chat_session": chat_session}
    return deps


async def model_random_create_chat_log(
    db: AsyncSession,
    deps: ChatLogDeps | None = None,
) -> ChatLogCreate:
    """If input deps, all dependencies for chat session must be provided"""
    # Prepare deps
    if deps is None:
        deps = await _create_chat_log_deps(db)
    dep_ids_map = create_dep_ids_map(deps, ChatLogDeps)

    # Model create chat log
    chat_session_id = dep_ids_map["chat_session"]
    prompt = random_lower_string()
    response_text = random_lower_string()

    return ChatLogCreate(
        chat_session_id=chat_session_id, prompt=prompt, response_text=response_text
    )


async def model_random_update_chat_log(
    db: AsyncSession,
    deps: ChatLogDeps | None = None,
) -> ChatLogUpdate:
    # Schemas for update is same as create
    chat_log_create = await model_random_create_chat_log(db, deps)
    chat_log_create = chat_log_create.model_dump()
    return ChatLogUpdate(**chat_log_create)


async def create_random_chat_log(
    db: AsyncSession,
    deps: ChatLogDeps | None = None,
) -> ChatLog:
    chat_log_in = await model_random_create_chat_log(db, deps)

    chat_log = await CRUD_chat_logs.create(db=db, obj_in=chat_log_in)
    return chat_log[0]
