from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseService
from app.db.database import get_session
from app.db.models import Menu, MenuCreate, MenuUpdate


class MenuCRUDService(BaseService[Menu, MenuCreate, MenuUpdate]):
    def __init__(self, db_session: AsyncSession):
        super(MenuCRUDService, self).__init__(Menu, db_session)


async def get_menu_service(
    db_session: AsyncSession = Depends(get_session),
) -> MenuCRUDService:
    return MenuCRUDService(db_session)
