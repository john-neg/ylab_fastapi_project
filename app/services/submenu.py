from aioredis import Redis
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.cache import get_cache
from app.services.base_cache_service import BaseCacheService
from app.services.base_crud_service import BaseCRUDService
from app.services.base_db_service import BaseDbService
from app.db.database import get_session
from app.db.models import Submenu, SubmenuCreate, SubmenuUpdate, SubmenuRead


class SubmenuModelService(BaseDbService[Submenu, SubmenuCreate, SubmenuUpdate]):
    """Model Service class for Submenu."""

    pass


class SubmenuCRUDService(BaseCRUDService[SubmenuRead, SubmenuCreate, SubmenuUpdate]):
    """CRUD service class for Submenu"""

    def add_attr(self, submenu: Submenu):
        data = {
            **submenu.dict(),
            "dishes_count": submenu.dishes.__len__(),
        }
        return self.read_model.parse_obj(data)


async def get_submenu_service(
    cache: Redis = Depends(get_cache),
    db_session: AsyncSession = Depends(get_session),
) -> SubmenuCRUDService:
    """
    The get_submenu_service function is a dependency function that returns an
    instance of the SubmenuCRUDService class. It takes in a database session
    and returns an instance of the SubmenuCRUDService class, which allows for
    CRUD operations on the submenus table in the database.
    """
    return SubmenuCRUDService(
        cache=BaseCacheService(cache),
        db_service=SubmenuModelService(Submenu, db_session),
        read_model=SubmenuRead,
        items_cache_list='submenus_list'
    )
