from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db


SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_user_ip_from_header(request: Request) -> str:
    client_ip = request.headers.get("X-Forwarded-For")
    return client_ip if client_ip is not None else "127.0.0.1"
