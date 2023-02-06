from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic.types import UUID4

from app.db.models import Menu, SubmenuCreate, SubmenuRead, SubmenuUpdate
from app.services.dependencies import validate_menu_model
from app.services.submenu import SubmenuCRUDService, get_submenu_service

router = APIRouter()


@router.get(
    "/",
    summary="Получить список подменю",
    response_model=list[SubmenuRead],
)
async def list_submenu(
    service: SubmenuCRUDService = Depends(get_submenu_service),
    menu: Menu = Depends(validate_menu_model),
) -> list[SubmenuRead]:
    return await service.list(menu_id=menu.id)


@router.get(
    "/{item_id}",
    summary="Получить детальную информацию о подменю",
    response_model=SubmenuRead,
)
async def get_submenu(
    item_id: UUID4,
    service: SubmenuCRUDService = Depends(get_submenu_service),
) -> SubmenuRead:
    return await service.get(item_id)


@router.post(
    "/",
    summary="Создать подменю",
    response_model=SubmenuRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_submenu(
    item_create: SubmenuCreate,
    service: SubmenuCRUDService = Depends(get_submenu_service),
    menu: Menu = Depends(validate_menu_model),
) -> SubmenuRead:
    return await service.create(item_create, menu_id=menu.id)


@router.patch(
    "/{item_id}",
    summary="Изменить подменю",
    response_model=SubmenuRead,
)
async def update_submenu(
    item_id: UUID4,
    item_update: SubmenuUpdate,
    service: SubmenuCRUDService = Depends(get_submenu_service),
) -> SubmenuRead:
    return await service.update(item_id, item_update)


@router.delete("/{item_id}", summary="Удалить подменю")
async def delete_submenu(
    item_id: UUID4,
    service: SubmenuCRUDService = Depends(get_submenu_service),
    menu: Menu = Depends(validate_menu_model),
) -> JSONResponse:
    return await service.delete(item_id, menu_id=menu.id)
