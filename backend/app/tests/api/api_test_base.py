from collections.abc import Awaitable, Callable
from uuid import uuid4

import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.base import CreateSchemaType, ModelType, UpdateSchemaType
from app.logs.logger import logger_test
from app.tests.test_base import BaseTest


class APITestBase(BaseTest):
    # For routes with no update endpoints
    skip_test_update = False

    @pytest.mark.asyncio
    async def test_get(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route: str,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
    ) -> None:
        obj = await obj_create(db)
        obj_id = obj.id

        assert obj_id

        response = await client.get(
            f"{settings.API_V1_STR}/{route}/{obj_id}",
            headers=superuser_token_headers,
        )

        assert response.status_code == 200
        content = response.json()
        assert jsonable_encoder(obj) == content

    @pytest.mark.asyncio
    async def test_get_not_found(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route: str,
    ) -> None:
        obj_id = uuid4()

        response = await client.get(
            f"{settings.API_V1_STR}/{route}/{obj_id}",
            headers=superuser_token_headers,
        )
        logger_test.error(response.json())
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_not_enough_permissions(
        self,
        client: AsyncClient,
        route: str,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
    ) -> None:
        obj = await obj_create(db)
        obj_id = obj.id

        assert obj_id

        response = await client.get(
            f"{settings.API_V1_STR}/{route}/{id}",
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route: str,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
    ) -> None:
        await obj_create(db)
        await obj_create(db)
        await obj_create(db)

        response = await client.get(
            f"{settings.API_V1_STR}/{route}/",
            headers=superuser_token_headers,
        )

        assert response.status_code == 200
        content = response.json()
        if "data" in content:
            content = content["data"]
        assert len(content) - self.num_initial_objs == 3

    @pytest.mark.asyncio
    async def test_create(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route: str,
        db: AsyncSession,
        obj_model_create: Callable[[AsyncSession], Awaitable[CreateSchemaType]],
    ) -> None:
        model_create = await obj_model_create(db)
        model_create_data = model_create.model_dump(mode="json")
        response = await client.post(
            f"{settings.API_V1_STR}/{route}/",
            headers=superuser_token_headers,
            json=model_create_data,
        )

        assert response.status_code == 200
        content = response.json()
        if isinstance(content, list):
            content = content[0]
        self.partial_fields_comparison(model_create_data, content)

    @pytest.mark.asyncio
    async def test_create_not_enough_permissions(
        self,
        client: AsyncClient,
        route: str,
        db: AsyncSession,
        obj_model_create: Callable[[AsyncSession], Awaitable[CreateSchemaType]],
    ) -> None:
        model_create = await obj_model_create(db)
        model_create_data = model_create.model_dump(mode="json")
        response = await client.post(
            f"{settings.API_V1_STR}/{route}/",
            json=model_create_data,
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_update(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route: str,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
        obj_model_update: Callable[[AsyncSession], Awaitable[UpdateSchemaType]],
    ) -> None:
        if self.skip_test_update:
            pytest.skip("test_update skipped since skip_test_update=True")
        obj = await obj_create(db)
        params = {"id": obj.id}

        model_update = await obj_model_update(db)
        model_update_data = model_update.model_dump(mode="json")
        response = await client.patch(
            f"{settings.API_V1_STR}/{route}/{params['id']}",
            headers=superuser_token_headers,
            json=model_update_data,
            params=params,
        )

        assert response.status_code == 200
        content = response.json()
        logger_test.error(content)

    @pytest.mark.asyncio
    async def test_update_not_found(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route: str,
        db: AsyncSession,
        obj_model_update: Callable[[AsyncSession], Awaitable[UpdateSchemaType]],
    ) -> None:
        if self.skip_test_update:
            pytest.skip("test_update skipped since skip_test_update=True")
        uuid = str(uuid4())
        params = {"id": uuid}

        model_update = await obj_model_update(db)
        model_update_data = model_update.model_dump(mode="json")
        response = await client.patch(
            f"{settings.API_V1_STR}/{route}/{params['id']}",
            headers=superuser_token_headers,
            json=model_update_data,
            params=params,
        )

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete(
        self,
        client: AsyncClient,
        superuser_token_headers: dict[str, str],
        route: str,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
    ) -> None:
        obj = await obj_create(db)
        params = {"id": obj.id}
        get_response = await client.get(
            f"{settings.API_V1_STR}/{route}/{params['id']}",
            headers=superuser_token_headers,
            params=params,
        )

        assert get_response.status_code == 200

        del_response = await client.delete(
            f"{settings.API_V1_STR}/{route}/{params['id']}",
            headers=superuser_token_headers,
            params=params,
        )

        assert del_response.status_code == 200

        not_found_get_response = await client.get(
            f"{settings.API_V1_STR}/{route}/{params['id']}",
            headers=superuser_token_headers,
            params=params,
        )

        assert not_found_get_response.status_code == 404
