from typing import List, Optional

from fastapi import Depends, APIRouter
from pydantic.types import UUID4
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.crud.base import BaseService
from app.db.database import get_session
from app.db.models import Menu, MenuCreate, MenuUpdate

router = APIRouter()


class MenuCRUDService(BaseService[Menu, MenuCreate, MenuUpdate]):
    def __init__(self, db_session: AsyncSession):
        super(MenuCRUDService, self).__init__(Menu, db_session)


async def get_crud_service(
    db_session: AsyncSession = Depends(get_session),
) -> MenuCRUDService:
    return MenuCRUDService(db_session)


@router.get("/", response_model=list[Menu])
async def list_menu(
    crud_service: MenuCRUDService = Depends(get_crud_service),
) -> List[Menu]:
    return await crud_service.list()


@router.get("/{item_id}", response_model=Menu)
async def get_menu(
    item_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_crud_service),
) -> Optional[Menu]:
    return await crud_service.get(item_id)


@router.post("/", response_model=Menu, status_code=status.HTTP_201_CREATED)
async def add_menu(
    item_create: MenuCreate,
    crud_service: MenuCRUDService = Depends(get_crud_service),
) -> Optional[Menu]:
    return await crud_service.create(item_create)


@router.patch("/{item_id}", response_model=Menu)
async def update_menu(
    item_id: UUID4,
    item_update: MenuUpdate,
    crud_service: MenuCRUDService = Depends(get_crud_service),
) -> Optional[Menu]:
    return await crud_service.update(item_id, item_update)


@router.delete("/{item_id}")
async def delete_menu(
    item_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_crud_service),
) -> JSONResponse:
    return await crud_service.delete(item_id)
