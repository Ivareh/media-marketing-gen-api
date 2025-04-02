import starlette.status as status

from app.exceptions.exception_base import MediaMarketAPIError


class UserWithNotEnoughPrivilegesError(MediaMarketAPIError):
    """Exception raised when user doesn't have enough privileges to perform an action."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        detail = "Cannot perform action with user. User doesn't have enough privileges to perform this action"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UserIsNotActiveError(MediaMarketAPIError):
    """Exception raised when user tries to perform actions and is not active."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        detail = (
            "Cannot perform action with user. "
            "User is not active. Please check your email for activation link"
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UserIsAlreadyActiveError(MediaMarketAPIError):
    """Exception raised when user tries to become actived, but is already actived."""

    def __init__(
        self,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        detail = "Cannot perform action with user. User is already actived."
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class SuperUserNotAllowedToDeleteSelfError(MediaMarketAPIError):
    """Exception raised when superuser tries to delete themselves."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        detail = "Cannot delete user. Superuser is not allowed to delete themselves"

        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class SuperUserNotAllowedToChangeActiveSelfError(MediaMarketAPIError):
    """Exception raised when superuser tries to change their active status."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        detail = (
            "Cannot change user active status. "
            "Superuser is not allowed to change their active status"
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class BadLoginCredentialsError(MediaMarketAPIError):
    """Exception raised for bad login credentials errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        detail = "Could not authorize. Invalid login credentials"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class InvalidPasswordError(MediaMarketAPIError):
    """Exception raised for invalid password errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        detail = "Could not authorize. Invalid password"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class NewPasswordIsSameError(MediaMarketAPIError):
    """Exception raised if the new password is the same as the old one."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str | None = None,
    ):
        detail = "Could not authorize. New password is the same as the old one"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class NotAuthenticatedError(MediaMarketAPIError):
    """Exception raised for not authenticated errors."""

    def __init__(
        self,
        *,
        detail: str,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UpdateExisitingMeValuesError(MediaMarketAPIError):
    """
    Exception raised when user tries to update their own values to
    be the same as their own existing values.
    """

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        detail = (
            "Cannot update user with value to be the same as their own existing values."
        )
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )


class UserEmailRequiredError(MediaMarketAPIError):
    """Exception raised for email is required for the operation errors."""

    def __init__(
        self,
        *,
        function_name: str | None = "Unknown function",
        class_name: str | None = None,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        detail = "Email is required for this operation"
        super().__init__(
            status_code=status_code,
            function_name=function_name,
            class_name=class_name,
            detail=detail,
        )
