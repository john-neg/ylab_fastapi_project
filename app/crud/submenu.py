from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseService
from app.db.database import get_session
from app.db.models import Submenu, SubmenuCreate, SubmenuUpdate


class SubmenuCRUDService(BaseService[Submenu, SubmenuCreate, SubmenuUpdate]):
    """CRUD Service class for Submenu."""

    def __init__(self, db_session: AsyncSession):
        super(SubmenuCRUDService, self).__init__(Submenu, db_session)


async def get_submenu_service(
    db_session: AsyncSession = Depends(get_session),
) -> SubmenuCRUDService:
    """
    The get_submenu_service function is a dependency function that returns an
    instance of the SubmenuCRUDService class. It takes in a database session
    and returns an instance of the SubmenuCRUDService class, which allows for
    CRUD operations on the submenus table in the database.
    """
    return SubmenuCRUDService(db_session)
