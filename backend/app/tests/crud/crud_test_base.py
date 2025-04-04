from collections.abc import Awaitable, Callable
from uuid import uuid4

import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CreateSchemaType, CRUDBase, ModelType, UpdateSchemaType
from app.exceptions import DbObjNotFoundError, DbTooManyItemsDeleteError
from app.tests.test_base import BaseTest


class CRUDTestBase(BaseTest):
    @pytest.mark.asyncio
    async def test_get(
        self,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
        crud: CRUDBase,
    ) -> None:
        obj: ModelType = await obj_create(db)
        obj_id = obj.id

        assert obj_id

        filter = {"id": obj_id}
        get_obj = await crud.get(db, filters=filter)

        assert get_obj
        assert jsonable_encoder(obj) == jsonable_encoder(
            get_obj[0]
        )  # Converts to dict and compare

    @pytest.mark.asyncio
    async def test_get_not_found(
        self,
        db: AsyncSession,
        crud: CRUDBase,
    ) -> None:
        uuid = uuid4()
        filter = {"id": uuid}

        with pytest.raises(DbObjNotFoundError):
            await crud.get(db, filters=filter)

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
        crud: CRUDBase,
    ) -> None:
        # Check there are no objs before creating
        all_objs = await crud.get_all(db)
        assert len(all_objs) - self.num_initial_objs == 0

        await obj_create(db)
        await obj_create(db)
        await obj_create(db)

        all_objs = await crud.get_all(db)

        assert all_objs
        assert len(all_objs) - self.num_initial_objs == 3

    @pytest.mark.asyncio
    async def test_create(
        self,
        db: AsyncSession,
        obj_model_create: Callable[[AsyncSession], Awaitable[CreateSchemaType]],
        crud: CRUDBase,
    ) -> None:
        model_create = await obj_model_create(db)
        created_obj = await crud.create(db, obj_in=model_create)

        assert created_obj
        self.partial_fields_comparison(
            model_create.model_dump(), jsonable_encoder(created_obj[0])
        )

    @pytest.mark.asyncio
    async def test_update(
        self,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
        obj_model_update: Callable[[AsyncSession], Awaitable[UpdateSchemaType]],
        crud: CRUDBase,
    ) -> None:
        # Create obj
        obj = await obj_create(db)
        original_data = jsonable_encoder(obj)
        obj_id = obj.id

        assert obj_id

        # Update model with update schema
        model_update = await obj_model_update(db)
        updated_obj = await crud.update(db, obj_id=obj_id, obj_in=model_update)
        update_obj_dict = jsonable_encoder(updated_obj)

        # Compare objects
        assert obj_id == updated_obj.id
        assert original_data != update_obj_dict
        self.partial_fields_comparison(model_update.model_dump(), update_obj_dict)

    @pytest.mark.asyncio
    async def test_update_not_found(
        self,
        db: AsyncSession,
        obj_model_update: Callable[[AsyncSession], Awaitable[UpdateSchemaType]],
        crud: CRUDBase,
    ) -> None:
        model_update = await obj_model_update(db)
        obj_id = uuid4()

        # Try update model with not found id
        with pytest.raises(DbObjNotFoundError):
            await crud.update(db, obj_id=obj_id, obj_in=model_update)

    @pytest.mark.asyncio
    async def test_delete(
        self,
        db: AsyncSession,
        obj_create: Callable[[AsyncSession], Awaitable[ModelType]],
        crud: CRUDBase,
    ) -> None:
        # Create and get obj
        obj = await obj_create(db)
        filter = {"id": obj.id}
        get_obj = await crud.get(db, filters=filter)

        assert get_obj

        # Delete obj
        delete_obj = await crud.delete(db, filters=filter)

        # Test deleted obj
        assert jsonable_encoder(get_obj) == jsonable_encoder(delete_obj)
        with pytest.raises(DbObjNotFoundError):
            await crud.get(db, filters=filter)

    @pytest.mark.asyncio
    async def test_delete_too_many(
        self,
        db: AsyncSession,
        obj_model_create: Callable[[AsyncSession], Awaitable[CreateSchemaType]],
        crud: CRUDBase,
    ) -> None:
        # Create objs with model
        model_create = await obj_model_create(db)
        created_obj = await crud.create(db, obj_in=model_create)
        filter = {"id": created_obj[0].id}

        assert created_obj

        # Try delete with limit 0
        with pytest.raises(DbTooManyItemsDeleteError):
            await crud.delete(db, filters=filter, max_deletion_limit=0)
