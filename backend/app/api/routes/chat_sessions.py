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
    ChatSessionCreate,
    ChatSessionPublic,
    FilterParams,
)
from app.crud import CRUD_chat_sessions

router = APIRouter(prefix="/chat_sessions", tags=["chat_sessions"])


@router.get(
    "/{chat_session_id}",
    response_model=ChatSessionPublic,
)
async def get_chat_session(
    chat_session_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Get chat session by value for `chat_session_id`.

    Returns the chat session.
    """

    chat_session_map = {"id": chat_session_id}
    chat_session = await CRUD_chat_sessions.get(db=db, filters=chat_session_map)

    return chat_session[0]


@router.get(
    "/",
    response_model=list[ChatSessionPublic],
)
async def get_all_chat_sessions(
    filter_params: Annotated[FilterParams, Query()],
    db: AsyncSession = Depends(get_db),
):
    """
    Get all chat sessions.

    Returns a list of all chat sessions.
    """

    all_chat_sessions = await CRUD_chat_sessions.get_all(
        db=db, filter_params=filter_params
    )

    return all_chat_sessions


@router.post(
    "/",
    response_model=list[ChatSessionPublic] | None,
)
async def create_chat_session(
    chat_sessions: ChatSessionCreate | list[ChatSessionCreate],
    return_nothing: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a list of chat_sessions.

    Returns the list of chat sessions.
    """
    created_chat_sessions = await CRUD_chat_sessions.create(
        db=db, obj_in=chat_sessions, return_nothing=return_nothing
    )

    return created_chat_sessions


@router.delete(
    "/{chat_session_id}",
    response_model=str,
)
async def delete_chat_session(
    chat_session_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a chat session by value for `chat_session_id`.

    Returns a message indicating the chat session was deleted.
    """

    chat_session_map = {"id": chat_session_id}
    await CRUD_chat_sessions.delete(db=db, filters=chat_session_map)

    return delete_return_msg(objs="Chat session", filters=chat_session_map).message
