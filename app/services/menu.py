from aioredis import Redis
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.cache import get_cache
from app.services.base_cache_service import BaseCacheService
from app.services.base_crud_service import BaseCRUDService
from app.services.base_db_service import BaseDbService
from app.db.database import get_session
from app.db.models import Menu, MenuCreate, MenuUpdate, MenuRead


class MenuModelService(BaseDbService[Menu, MenuCreate, MenuUpdate]):
    """Model Service class for Menu."""

    pass


class MenuCRUDService(BaseCRUDService[MenuRead, MenuCreate, MenuUpdate]):
    """CRUD service class for Menu"""

    def add_attr(self, menu: Menu):
        data = {
            **menu.dict(),
            "submenus_count": len(menu.submenus),
            "dishes_count": sum(
                [len(submenu.dishes) for submenu in menu.submenus]
            )
        }
        return self.read_model.parse_obj(data)


async def get_menu_service(
    cache: Redis = Depends(get_cache),
    db_session: AsyncSession = Depends(get_session),
) -> MenuCRUDService:
    """
    The get_menu_service function is a dependency function that returns an
    instance of the MenuCRUDService class. It takes in a db_session parameter,
    which is an async session from the fastapi dependency injection framework.
    """
    return MenuCRUDService(
        cache=BaseCacheService(cache),
        db_service=MenuModelService(Menu, db_session),
        read_model=MenuRead,
        items_cache_list='menus_list'
    )
