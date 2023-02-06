from dataclasses import dataclass
from typing import Generic, TypeVar

from fastapi.responses import JSONResponse
from pydantic.types import UUID4

from app.db.models import DefaultReadBase
from app.services.base_cache_service import BaseCacheService
from app.services.base_db_service import (
    BaseDbService,
    CreateSchemaType,
    ModelType,
    UpdateSchemaType,
)

ReadSchemaType = TypeVar("ReadSchemaType", bound=DefaultReadBase)


@dataclass
class BaseCRUDService(
    Generic[ReadSchemaType, CreateSchemaType, UpdateSchemaType],
):
    cache: BaseCacheService
    db_service: BaseDbService
    read_model: type[ReadSchemaType]
    items_cache_list: str

    def process_db_data(self, item: ModelType) -> ReadSchemaType:
        """
        The process_db_data function takes in a ModelType object and returns
        the data in that object as a dictionary. This function is used to
        convert the database data into JSON format.
        """
        return self.read_model.parse_obj(item.dict())

    async def list(self, **kwargs) -> list[ReadSchemaType]:
        """The list function returns all object items from the database."""
        items_list = await self.cache.get(self.items_cache_list)
        if not items_list:
            obj_list = await self.db_service.list(**kwargs)
            items_list = [self.process_db_data(item) for item in obj_list]
            await self.cache.set(self.items_cache_list, items_list)
        return items_list

    async def get(self, item_id: UUID4) -> ReadSchemaType:
        """
        The get function is used to retrieve a single item. It takes an id as
        input and returns the corresponding object. If no such object exists,
        it returns None.
        """
        item = await self.cache.get(str(item_id))
        if not item:
            obj = await self.db_service.get(item_id)
            item = self.process_db_data(obj)
            await self.cache.set(str(item_id), item)
        return item

    async def create(
        self,
        item_create_schema: CreateSchemaType,
        **kwargs,
    ) -> ReadSchemaType:
        """
        The create function creates a new item in the database, set it to cache
        and returns it. It also deletes all related cached items, so that they
        can be reloaded from the database.
        """
        obj = await self.db_service.create(
            item_create_schema,
            **kwargs,
        )
        item = self.process_db_data(obj)
        for key in [*kwargs.values(), self.items_cache_list]:
            await self.cache.delete(str(key))
        await self.cache.set(str(obj.id), item)
        return item

    async def update(
        self,
        item_id: UUID4,
        item_update_schema: UpdateSchemaType,
    ) -> ReadSchemaType:
        """
        The update function updates an existing item in the database and cache.
        It returns a dictionary with all the fields from that object.
        """
        obj = await self.db_service.update(item_id, item_update_schema)
        item = self.process_db_data(obj)
        await self.cache.set(str(item_id), item)
        await self.cache.delete(self.items_cache_list)
        return item

    async def delete(self, item_id: UUID4, **kwargs) -> JSONResponse:
        """
        The delete function is used to delete an item from the database and
        all related cached items. It takes in an id as an argument and
        returns the JSONResponse containing a message confirming that object
        was deleted.
        """
        for key in [*kwargs.values(), self.items_cache_list, str(item_id)]:
            await self.cache.delete(str(key))
        return await self.db_service.delete(item_id)
