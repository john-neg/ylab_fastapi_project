from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import BaseService
from app.db.database import get_session
from app.db.models import Dish, DishCreate, DishUpdate


class DishCRUDService(BaseService[Dish, DishCreate, DishUpdate]):
    def __init__(self, db_session: AsyncSession):
        super(DishCRUDService, self).__init__(Dish, db_session)


async def get_dish_service(
    db_session: AsyncSession = Depends(get_session),
) -> DishCRUDService:
    return DishCRUDService(db_session)
