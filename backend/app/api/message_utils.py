from typing import Any

from app.core.schemas import Message


def delete_return_msg(
    objs: str,
    filters: dict[str, Any],
) -> Message:
    return Message(message=f"{objs} with filters '{filters}' was deleted successfully.")
