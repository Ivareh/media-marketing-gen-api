from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


class MediaMarketAPIError(HTTPException):
    """
    Base class for exceptions in the Media Marketing Generating API module.

    ``function_name`` makes it easier to debug. It can be provided with `function.__name__`.
    """

    def __init__(
        self,
        *,
        status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        detail: str | None = "An error occured for this Media Market API request",
        headers: dict[str, str] | None = None,
    ):
        if class_name is not None and function_name is not None:
            function_name = f"{class_name}.{function_name}"
        status_code = status_code
        function_name = function_name
        detail = (
            f"Media market: status={status_code} : function={function_name} : {detail}"
        )
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )
