from fastapi import Depends
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseService
from app.db.database import get_session
from app.db.models import Submenu, SubmenuCreate, SubmenuUpdate, Dish


class SubmenuCRUDService(BaseService[Submenu, SubmenuCreate, SubmenuUpdate]):
    def __init__(self, db_session: AsyncSession):
        super(SubmenuCRUDService, self).__init__(Submenu, db_session)


async def get_submenu_service(
    db_session: AsyncSession = Depends(get_session),
) -> SubmenuCRUDService:
    return SubmenuCRUDService(db_session)
