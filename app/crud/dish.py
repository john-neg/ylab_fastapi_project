from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseService
from app.db.database import get_session
from app.db.models import Dish, DishCreate, DishUpdate


class DishCRUDService(BaseService[Dish, DishCreate, DishUpdate]):
    """CRUD Service class for Dish."""

    def __init__(self, db_session: AsyncSession):
        super(DishCRUDService, self).__init__(Dish, db_session)


async def get_dish_service(
    db_session: AsyncSession = Depends(get_session),
) -> DishCRUDService:
    """
    The get_dish_service function returns a DishCRUDService object.
    The DishCRUDService class is defined in the dish_crud_service module and
    is used to create, read, update and delete dishes from the database.
    """
    return DishCRUDService(db_session)
