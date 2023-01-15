from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic.types import UUID4
from starlette import status
from starlette.responses import JSONResponse

from app.crud.dependencies import validate_menu_model
from app.crud.submenu import SubmenuCRUDService, get_submenu_service
from app.db.models import Submenu, SubmenuCreate, SubmenuUpdate, Menu, SubmenuRead

router = APIRouter()






@router.get("/", response_model=list[Submenu])
async def list_submenu(
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
    menu: Menu = Depends(validate_menu_model),
) -> List[Submenu]:
    return await crud_service.list(menu_id=menu.id)


@router.get("/{item_id}", response_model=Submenu)
async def get_submenu(
    item_id: UUID4,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
) -> Optional[Submenu]:
    return await crud_service.get(item_id)


@router.post("/", response_model=Submenu, status_code=status.HTTP_201_CREATED)
async def add_submenu(
    item_create: SubmenuCreate,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
    menu: Menu = Depends(validate_menu_model),
) -> Optional[Submenu]:
    return await crud_service.create(item_create, menu_id=menu.id)


@router.patch("/{item_id}", response_model=Submenu)
async def update_submenu(
    item_id: UUID4,
    item_update: SubmenuUpdate,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
) -> Optional[Submenu]:
    return await crud_service.update(item_id, item_update)


@router.delete("/{item_id}")
async def delete_submenu(
    item_id: UUID4,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
) -> JSONResponse:
    return await crud_service.delete(item_id)
