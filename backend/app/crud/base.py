from collections.abc import Sequence
from contextlib import asynccontextmanager
from typing import Any, Generic, Literal, TypeVar, overload

from pydantic import UUID4, BaseModel, TypeAdapter
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, asc, delete, desc, func, select

from app.core.schemas import FilterParams
from app.exceptions import (
    DbObjAlreadyExistsError,
    DbObjNotFoundError,
    DbTooManyItemsDeleteError,
    GeneralDbError,
)

ModelType = TypeVar("ModelType", bound=Any)
SchemaType = TypeVar("SchemaType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        model: type[ModelType],
        schema: type[SchemaType],
        create_schema: type[CreateSchemaType],
    ):
        """
        Async CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Transactions begin explicitly for performance reasons (short time db connections).

        :param model: ModelType
            A SQLAlchemy schema class
        :param schema: SchemaType
            A Pydantic schema class
        :param create_schema: CreateSchemaType
            Create schema for Pydantic class
        """
        self.model = model
        self.schema = schema
        self.create_schema = create_schema

        self.validate = TypeAdapter(SchemaType | list[SchemaType]).validate_python

    @asynccontextmanager
    async def _optional_transaction(self, db: AsyncSession):
        """Context manager that reuses existing transaction or starts a new one."""
        if not db.in_transaction():
            async with db.begin():
                yield
        else:
            yield

    def _apply_filter_params(
        self, stmt: Select, *, model: type[ModelType], filter_params: FilterParams
    ) -> Select:
        """
        Some modifications, but retrieved from: https://github.com/igorbenav/fastcrud/blob/main/fastcrud/crud/fast_crud.py#L762

        Apply sorting to a SQLAlchemy query based on specified column names and sort orders.

        Args:
            stmt: The SQLAlchemy `Select` statement to which sorting will be applied.
            sort_columns: A single column name or a list of column names on which to apply sorting.
            sort_orders: A single sort order (`"asc"` or `"desc"`) or a list of sort orders corresponding
                to the columns in `sort_columns`. If not provided, defaults to `"asc"` for each column.

        Note:
            This method modifies the passed `Select` statement by applying the `order_by` clause
            based on the provided column names and sort orders.
        """
        if filter_params.offset is not None:
            stmt = stmt.offset(filter_params.offset)
        if filter_params.limit is not None:
            stmt = stmt.limit(filter_params.limit)

        sort_orders = filter_params.sort_orders
        sort_columns = filter_params.sort_columns

        if sort_orders and not sort_columns:
            raise ValueError("Sort orders provided without corresponding sort columns.")

        if sort_columns:
            if not isinstance(sort_columns, list):
                sort_columns = [sort_columns]

            if sort_orders:
                if not isinstance(sort_orders, list):
                    sort_orders = [sort_orders] * len(sort_columns)
                if len(sort_columns) != len(sort_orders):
                    raise ValueError(
                        "The length of sort_columns and sort_orders must match."
                    )

                for _, order in enumerate(sort_orders):
                    if order not in ["asc", "desc"]:
                        raise ValueError(
                            f"Invalid sort order: {order}. Only 'asc' or 'desc' are allowed."
                        )

            validated_sort_orders = (
                ["asc"] * len(sort_columns) if not sort_orders else sort_orders
            )

            for idx, column_name in enumerate(sort_columns):
                column = getattr(model, column_name, None)
                if not column:
                    raise ArgumentError(f"Invalid column name: {column_name}")

                order = validated_sort_orders[idx]
                stmt = stmt.order_by(asc(column) if order == "asc" else desc(column))

        return stmt

    async def _create_bulk(
        self,
        db: AsyncSession,
        *,
        model_dict_list: list[dict[str, Any]],
        return_nothing: bool = False,
    ) -> Sequence[ModelType] | None:
        """return_nothing=True improves performance"""

        create_stmt = insert(self.model)
        created_objs = None
        try:
            created_objs_result = None
            async with self._optional_transaction(db):
                if return_nothing:
                    await db.execute(create_stmt, model_dict_list)
                else:
                    create_stmt = create_stmt.returning(self.model)
                    created_objs_result = await db.execute(create_stmt, model_dict_list)
            if created_objs_result is not None:
                created_objs = created_objs_result.scalars().all()
        except Exception as e:
            reason = str(e.args[0])
            if "duplicate key value violates unique constraint" in reason:
                raise DbObjAlreadyExistsError(
                    model_table_name=self.model.__tablename__,
                    obj_indicator=model_dict_list,
                    function_name=self.create.__name__,
                    class_name=self.__class__.__name__,
                )
            else:
                raise GeneralDbError(
                    model_table_name=self.model.__tablename__,
                    function_name=self.create.__name__,
                    class_name=self.__class__.__name__,
                    exception=e,
                )

        return created_objs

    async def _get_multi(
        self,
        db: AsyncSession,
        filters: dict[str, Any] | None = None,
        *,
        filter_params: FilterParams | None = None,
    ) -> Sequence[ModelType] | None:
        stmt = select(self.model)

        if filters is not None:
            stmt = stmt.filter_by(**filters)

        if filter_params:
            stmt = self._apply_filter_params(
                stmt, model=self.model, filter_params=filter_params
            )

        async with self._optional_transaction(db):
            db_objs_result = await db.execute(stmt)

        db_objs: Sequence[ModelType] = db_objs_result.scalars().all()

        return db_objs

    async def get(
        self,
        db: AsyncSession,
        filters: dict[str, Any] | None = None,
        *,
        filter_params: FilterParams | None = None,
    ) -> Sequence[ModelType]:
        """Raises `DbObjNotFoundError` if no objects are found"""

        db_objs = await self._get_multi(db, filters, filter_params=filter_params)

        if not db_objs:
            raise DbObjNotFoundError(
                model_table_name=self.model.__tablename__,
                obj_indicator=filters,
                function_name=self.get.__name__,
                class_name=self.__class__.__name__,
            )
        self.validate(db_objs)
        return db_objs

    async def get_all(
        self,
        db: AsyncSession,
        *,
        filter_params: FilterParams | None = None,
    ) -> Sequence[ModelType]:
        db_objs = await self._get_multi(db, filter_params=filter_params)

        if not db_objs:
            return []

        self.validate(db_objs)
        return db_objs

    async def get_count_all(
        self,
        db: AsyncSession,
    ) -> int:
        count_statement = select(func.count()).select_from(self.model)
        async with self._optional_transaction(db):
            count = await db.execute(count_statement)

        return count.one()[0]

    # Handle different return_nothing
    @overload
    async def create(
        self,
        db: ...,
        *,
        obj_in: ...,
        return_nothing: Literal[False] = False,
    ) -> list[ModelType]:
        ...

    @overload
    async def create(
        self,
        db: ...,
        *,
        obj_in: ...,
        return_nothing: Literal[True],
    ) -> None:
        ...

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType | list[CreateSchemaType],
        return_nothing: bool = False,
    ) -> Sequence[ModelType] | None:
        """
        return_nothing=True improves performance
        """

        if isinstance(obj_in, list):
            model_dict_list = [obj.model_dump() for obj in obj_in]
        else:
            model_dict_list = [obj_in.model_dump()]

        created_objects = await self._create_bulk(
            db, model_dict_list=model_dict_list, return_nothing=return_nothing
        )

        if not created_objects:
            if not return_nothing:
                raise GeneralDbError(
                    model_table_name=self.model.__tablename__,
                    function_name=self.create.__name__,
                    class_name=self.__class__.__name__,
                    detail="No db objects was returned, though it was supposed to",
                )
            return None

        self.validate(created_objects)
        return created_objects

    async def update(
        self,
        db: AsyncSession,
        *,
        obj_id: UUID4,
        obj_in: UpdateSchemaType,
    ) -> ModelType:
        """Update object by id (pk) for object"""

        update_data = obj_in.model_dump()

        filter = {"id": obj_id}
        stmt = select(self.model).filter_by(**filter)
        async with self._optional_transaction(db):
            db_objs_result = await db.execute(stmt)
            db_obj: ModelType | None = db_objs_result.scalar()

            if not db_obj:
                raise DbObjNotFoundError(
                    model_table_name=self.model.__tablename__,
                    obj_indicator=filter,
                    function_name=self.update.__name__,
                    class_name=self.__class__.__name__,
                )

            for field in update_data:
                setattr(db_obj, field, update_data[field])

            await db.flush()
            await db.refresh(db_obj)
        self.validate(db_obj)
        return db_obj

    async def delete(
        self,
        db: AsyncSession,
        *,
        filters: dict[str, Any],
        max_deletion_limit: int = 12,
        filter_params: FilterParams | None = None,
    ) -> Sequence[ModelType]:
        """Can delete multiple objects, but with a specified limit"""

        stmt = select(self.model).filter_by(**filters)
        if filter_params and filter_params.sort_columns:
            stmt = self._apply_filter_params(
                stmt, model=self.model, filter_params=filter_params
            )

        async with self._optional_transaction(db):
            db_obj_result = await db.execute(stmt)
            db_objs = db_obj_result.scalars().all()

            if not db_objs:
                raise DbObjNotFoundError(
                    model_table_name=self.model.__tablename__,
                    obj_indicator=filters,
                    function_name=self.delete.__name__,
                    class_name=self.__class__.__name__,
                )
            if len(db_objs) > max_deletion_limit:  # Arbitrary number, not too large
                raise DbTooManyItemsDeleteError(
                    max_deletion_number=max_deletion_limit,
                    model_table_name=self.model.__tablename__,
                    function_name=self.delete.__name__,
                    class_name=self.__class__.__name__,
                )

            stmt = delete(self.model).filter_by(**filters)
            await db.execute(stmt)
            await db.flush()
        self.validate(db_objs)
        return db_objs
