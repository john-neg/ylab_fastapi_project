from typing import List, Optional

from fastapi import Depends, APIRouter
from pydantic.types import UUID4
from starlette import status
from starlette.responses import JSONResponse

from app.db.models import Menu, MenuCreate, MenuUpdate
from ..services.menu import MenuCRUDService, get_menu_service

router = APIRouter()





@router.get("/", response_model=list[Menu])
async def list_menu(
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> List[Menu]:
    return await crud_service.list()


@router.get("/{menu_id}", response_model=Menu)
async def get_menu(
    menu_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> Optional[Menu]:
    return await crud_service.get(menu_id)


@router.post("/", response_model=Menu, status_code=status.HTTP_201_CREATED)
async def add_menu(
    item_create: MenuCreate,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> Optional[Menu]:
    return await crud_service.create(item_create)


@router.patch("/{menu_id}", response_model=Menu)
async def update_menu(
    menu_id: UUID4,
    item_update: MenuUpdate,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> Optional[Menu]:
    return await crud_service.update(menu_id, item_update)


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> JSONResponse:
    return await crud_service.delete(menu_id)
