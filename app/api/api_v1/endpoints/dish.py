from typing import List, Optional

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic.types import UUID4

from app.crud.dependencies import get_submenu_id, validate_submenu_model
from app.crud.dish import DishCRUDService, get_dish_service
from app.db.models import Dish, DishCreate, DishRead, DishUpdate, Menu

router = APIRouter()


@router.get("/", response_model=list[DishRead])
async def list_dish(
    crud_service: DishCRUDService = Depends(get_dish_service),
    submenu_id: str = Depends(get_submenu_id),
) -> List[Dish]:
    return await crud_service.list(submenu_id=submenu_id)


@router.get("/{item_id}", response_model=DishRead)
async def get_dish(
    item_id: UUID4,
    crud_service: DishCRUDService = Depends(get_dish_service),
) -> Optional[Dish]:
    return await crud_service.get(item_id)


@router.post("/", response_model=DishRead, status_code=status.HTTP_201_CREATED)
async def add_dish(
    item_create: DishCreate,
    crud_service: DishCRUDService = Depends(get_dish_service),
    submenu: Menu = Depends(validate_submenu_model),
) -> Optional[Dish]:
    return await crud_service.create(item_create, submenu_id=submenu.id)


@router.patch("/{item_id}", response_model=DishRead)
async def update_dish(
    item_id: UUID4,
    item_update: DishUpdate,
    crud_service: DishCRUDService = Depends(get_dish_service),
) -> Optional[Dish]:
    return await crud_service.update(item_id, item_update)


@router.delete("/{item_id}")
async def delete_dish(
    item_id: UUID4,
    crud_service: DishCRUDService = Depends(get_dish_service),
) -> JSONResponse:
    return await crud_service.delete(item_id)
