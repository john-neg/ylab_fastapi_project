from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic.types import UUID4

from app.db.models import Dish, DishCreate, DishRead, DishUpdate, Menu, Submenu
from app.services.dependencies import (
    get_submenu_id,
    validate_menu_model,
    validate_submenu_model,
)
from app.services.dish import DishCRUDService, get_dish_service

router = APIRouter()


@router.get('/', summary='Получить список блюд', response_model=list[DishRead])
async def list_dish(
    service: DishCRUDService = Depends(get_dish_service),
    submenu_id: str = Depends(get_submenu_id),
) -> list[dict]:
    return await service.list(submenu_id=submenu_id)


@router.get(
    '/{item_id}',
    summary='Получить детальную информацию о блюде',
    response_model=DishRead,
)
async def get_dish(
    item_id: UUID4,
    service: DishCRUDService = Depends(get_dish_service),
) -> Dish | None:
    return await service.get(item_id)


@router.post(
    '/',
    summary='Создать блюдо',
    response_model=DishRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_dish(
    item_create_schema: DishCreate,
    service: DishCRUDService = Depends(get_dish_service),
    submenu: Submenu = Depends(validate_submenu_model),
) -> Dish | None:
    return await service.create(item_create_schema, submenu_id=submenu.id)


@router.patch('/{item_id}', summary='Изменить блюдо', response_model=DishRead)
async def update_dish(
    item_id: UUID4,
    item_update_schema: DishUpdate,
    service: DishCRUDService = Depends(get_dish_service),
) -> Dish | None:
    return await service.update(item_id, item_update_schema)


@router.delete('/{item_id}', summary='Удалить блюдо')
async def delete_dish(
    item_id: UUID4,
    service: DishCRUDService = Depends(get_dish_service),
    submenu: Submenu = Depends(validate_submenu_model),
    menu: Menu = Depends(validate_menu_model),
) -> JSONResponse:
    return await service.delete(
        item_id,
        submenu_id=submenu.id,
        menu_id=menu.id,
    )
