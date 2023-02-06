from aioredis import Redis
from fastapi import Depends

from app.db.cache import get_cache
from app.db.database import get_session
from app.db.models import Dish, DishCreate, DishRead, DishUpdate
from app.services.base_cache_service import BaseCacheService
from app.services.base_crud_service import BaseCRUDService
from app.services.base_db_service import BaseDbService


class DishModelService(BaseDbService[Dish, DishCreate, DishUpdate]):
    """Model service class for Dish."""

    pass


class DishCRUDService(BaseCRUDService[DishRead, DishCreate, DishUpdate]):
    """CRUD service class for Dish"""

    pass


async def get_dish_service(
    cache: Redis = Depends(get_cache),
    session=Depends(get_session),
) -> DishCRUDService:
    """
    The get_dish_service function returns a DishCRUDService object. The
    DishCRUDService class is used to create, read, update and delete dishes.
    """
    return DishCRUDService(
        cache=BaseCacheService(cache),
        db_service=DishModelService(Dish, session),
        read_model=DishRead,
        items_cache_list="dishes_list",
    )
