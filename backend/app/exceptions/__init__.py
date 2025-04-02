from app.exceptions.exception_base import MediaMarketAPIError
from app.exceptions.model_exceptions.db_exceptions import (
    DbObjAlreadyExistsError,
    DbObjNotFoundError,
    DbTooManyItemsDeleteError,
    GeneralDbError,
)
from app.exceptions.model_exceptions.user_exceptions import (
    BadLoginCredentialsError,
    InvalidPasswordError,
    NewPasswordIsSameError,
    NotAuthenticatedError,
    SuperUserNotAllowedToChangeActiveSelfError,
    SuperUserNotAllowedToDeleteSelfError,
    UpdateExisitingMeValuesError,
    UserEmailRequiredError,
    UserIsAlreadyActiveError,
    UserIsNotActiveError,
    UserWithNotEnoughPrivilegesError,
)
