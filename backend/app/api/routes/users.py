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
    Message,
    UsersPublic,
    UserCreate,
    UserPublic,
    FilterParams,
    UserUpdate,
)
from app.crud import CRUD_users

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/{user_id}",
    response_model=UserPublic,
)
async def get_user(
    user_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Get chat session by value for `user_id`.

    Always returns one user.
    """

    user_map = {"id": user_id}
    user = await CRUD_users.get(db=db, filters=user_map)

    user_public = UserPublic.model_validate(user[0])

    return user_public


@router.get("/", response_model=UsersPublic)
async def get_all_users(
    filter_params: Annotated[FilterParams, Query()],
    db: AsyncSession = Depends(get_db),
):
    """
    Get all users.

    Returns a list of all users.
    """

    all_users = await CRUD_users.get_all(db=db, filter_params=filter_params)

    user_public_list: list[UserPublic] = [
        UserPublic.model_validate(user) for user in all_users
    ]

    users_count = await CRUD_users.get_count_all(db)

    users_public = UsersPublic(data=user_public_list, count=users_count)

    return users_public


@router.post(
    "/",
    response_model=UserPublic,
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a user."""
    user_obj = await CRUD_users.create(db=db, obj_in=user)

    user_public = UserPublic.model_validate(user_obj[0])

    return user_public


@router.patch(
    "/{user_id}",
    response_model=UserPublic,
)
async def update_user(
    user_id: UUID4,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update a user by value for `user_id`.

    Returns the updated user.
    """
    updated_user = await CRUD_users.update(db=db, obj_id=user_id, obj_in=user_update)

    updated_user_public = UserPublic.model_validate(updated_user)

    return updated_user_public


@router.delete(
    "/{user_id}",
    response_model=Message,
)
async def delete_user(
    user_id: UUID4,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a user by value for `user_id`.

    Returns a message indicating the chat session was deleted.
    """

    filter = {"id": user_id}
    await CRUD_users.delete(db=db, filters=filter)

    return delete_return_msg(objs="User", filters={"id": user_id})
