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
    ChatLogCreate,
    ChatLogPublic,
    FilterParams,
)
from app.crud import CRUD_chat_logs

router = APIRouter(prefix="/chat_logs", tags=["chat_logs"])


@router.get(
    "/{chat_log_id}",
    response_model=ChatLogPublic,
)
async def get_chat_log(
    chat_log_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Get chat log by value for `chat_log_id`.

    Returns the chat log.
    """

    chat_log_map = {"id": chat_log_id}
    chat_log = await CRUD_chat_logs.get(db=db, filters=chat_log_map)

    return chat_log[0]


@router.get(
    "/",
    response_model=list[ChatLogPublic],
)
async def get_all_chat_logs(
    filter_params: Annotated[FilterParams, Query()],
    db: AsyncSession = Depends(get_db),
):
    """
    Get all chat logs.

    Returns a list of all chat logs.
    """

    all_chat_logs = await CRUD_chat_logs.get_all(db=db, filter_params=filter_params)

    return all_chat_logs


@router.post(
    "/",
    response_model=list[ChatLogPublic] | None,
)
async def create_chat_log(
    chat_logs: ChatLogCreate | list[ChatLogCreate],
    return_nothing: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a list of chat logs.

    Returns the list of chat logs.
    """
    created_chat_logs = await CRUD_chat_logs.create(
        db=db, obj_in=chat_logs, return_nothing=return_nothing
    )

    return created_chat_logs


@router.delete(
    "/{chat_log_id}",
    response_model=str,
)
async def delete_chat_log(
    chat_log_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a chat log by value for `chat_log_id`.

    Returns a message indicating the chat log was deleted.
    """

    chat_log_map = {"id": chat_log_id}
    await CRUD_chat_logs.delete(db=db, filters=chat_log_map)

    return delete_return_msg(objs="Chat log", filters=chat_log_map).message
