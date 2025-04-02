import random
import string
from typing import Any, TypedDict, TypeVar, get_type_hints
from uuid import uuid4

from httpx import AsyncClient
from pydantic import UUID4, BaseModel

from app.core.config import settings
from app.exceptions import NotAuthenticatedError

Schema = TypeVar("Schema", bound=BaseModel)


class ModelDeps(TypedDict):
    """Base Class for ModelType dependencies"""


def random_lower_string(*, small_string: bool | None = None) -> str:
    random_lower_string = "".join(random.choices(string.ascii_lowercase, k=32))
    if small_string:
        random_lower_string = random_lower_string[:5]
    return random_lower_string


def random_uuid() -> UUID4:
    return uuid4()


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_full_name() -> str:
    first_name = random_lower_string(small_string=True).capitalize()
    surname = random_lower_string(small_string=True).capitalize()
    return first_name + " " + surname


async def get_superuser_token_headers() -> dict[str, str]:
    """Make a request to entra id with provided secret to get auth headers"""
    async with AsyncClient() as client:
        azure_response = await client.post(
            url=f"https://login.microsoftonline.com/{settings.FIRST_SUPERUSER_TENANT_ID}/oauth2/v2.0/token",
            data={
                "grant_type": "client_credentials",
                "client_id": settings.OPENAPI_CLIENT_ID,  # the ID of the app reg you created the secret for
                "client_secret": settings.FIRST_SUPERUSER_CLIENT_SECRET,  # the secret you created
                "scope": f"api://{settings.APP_CLIENT_ID}/.default",  # note: NOT .user_impersonation
            },
        )
        if not azure_response.is_success:
            raise NotAuthenticatedError(
                detail=azure_response.json()["error_description"],
                function_name=get_superuser_token_headers.__name__,
                status_code=azure_response.status_code,
            )

        token = azure_response.json()["access_token"]

        return {"Authorization": f"Bearer {token}"}


def _raise_if_partial_deps(deps: ModelDeps, model_deps_cls: type[ModelDeps]):
    """Validate that all non-optional keys in the TypedDict are present and non-null"""
    required_keys = get_type_hints(model_deps_cls).keys()

    missing = [k for k in required_keys if k not in deps]
    if missing:
        raise ValueError(f"Missing required dependencies: {missing}")

    null_values = [k for k in required_keys if deps.get(k) is None]
    if null_values:
        raise ValueError(f"Null values found in dependencies: {null_values}")


def create_dep_ids_map(
    deps: ModelDeps, model_deps_cls: type[ModelDeps]
) -> dict[str, Any]:
    # Check deps
    _raise_if_partial_deps(deps, model_deps_cls)
    ids = {}
    for dep_name, dep_obj in deps.items():
        dep_id = dep_obj.id  # type: ignore
        assert id is not None
        ids[dep_name] = dep_id

    return ids
