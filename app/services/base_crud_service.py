from dataclasses import dataclass
from typing import TypeVar, Type, Generic

from pydantic.types import UUID4

from app.db.models import DefaultReadBase
from app.services.base_cache_service import BaseCacheService
from app.services.base_db_service import BaseDbService, UpdateSchemaType, \
    CreateSchemaType, ModelType

ReadSchemaType = TypeVar("ReadSchemaType", bound=DefaultReadBase)


@dataclass
class BaseCRUDService(
    Generic[ReadSchemaType, CreateSchemaType, UpdateSchemaType]
):
    cache: BaseCacheService
    db_service: BaseDbService
    read_model: Type[ReadSchemaType]
    items_cache_list: str

    def add_attr(self, item: ModelType):
        return self.read_model.parse_obj(item.dict())

    async def list(self, **kwargs) -> list[dict]:
        """The list function returns all object items from the database."""
        items_list = await self.cache.get(self.items_cache_list)
        if not items_list:
            obj_list = await self.db_service.list(**kwargs)
            items_list = [self.add_attr(item) for item in obj_list]
            await self.cache.set(self.items_cache_list, items_list)
        return items_list

    async def get(self, item_id: UUID4):
        """
        The get function is used to retrieve a single item. It takes an id as
        input and returns the corresponding object. If no such object exists,
        it returns None.
        """
        item = await self.cache.get(str(item_id))
        if not item:
            obj = await self.db_service.get(item_id)
            item = self.add_attr(obj)
            await self.cache.set(str(item_id), item)
        return item

    async def create(self, item_create_schema: CreateSchemaType, **kwargs):
        """
        The create function creates a new item in the database, set it to cache
        and returns it. It also deletes all related cached items, so that they
        can be reloaded from the database.
        """
        obj = await self.db_service.create(
            item_create_schema, **kwargs
        )
        item = self.add_attr(obj)
        for key in [*kwargs.values(), self.items_cache_list]:
            await self.cache.delete(str(key))
        await self.cache.set(str(obj.id), item)
        return item

    async def update(
        self, item_id: UUID4, item_update_schema: UpdateSchemaType
    ):
        """
        The update function updates an existing item in the database and cache.
        It returns a dictionary with all the fields from that object.
        """
        obj = await self.db_service.update(item_id, item_update_schema)
        item = self.add_attr(obj)
        await self.cache.set(str(obj.id), item)
        await self.cache.delete(self.items_cache_list)
        return item

    async def delete(self, item_id: UUID4, **kwargs):
        """
        The delete function is used to delete an item from the database and
        all related cached items. It takes in an id as an argument and
        returns the JSONResponse containing a message confirming that object
        was deleted.
        """
        for key in [*kwargs.values(), self.items_cache_list, str(item_id)]:
            await self.cache.delete(str(key))
        return await self.db_service.delete(item_id)