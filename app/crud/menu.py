from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseService
from app.db.database import get_session
from app.db.models import Menu, MenuCreate, MenuUpdate


class MenuCRUDService(BaseService[Menu, MenuCreate, MenuUpdate]):
    """CRUD Service class for Menu."""

    def __init__(self, db_session: AsyncSession):
        super(MenuCRUDService, self).__init__(Menu, db_session)


async def get_menu_service(
    db_session: AsyncSession = Depends(get_session),
) -> MenuCRUDService:
    """
    The get_menu_service function is a dependency function that returns an
    instance of the MenuCRUDService class. It takes in a db_session parameter,
    which is an async session from the fastapi dependency injection framework.
    """
    return MenuCRUDService(db_session)
