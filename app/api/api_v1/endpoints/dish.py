from typing import Optional, List

from fastapi import APIRouter, Depends
from pydantic.types import UUID4
from fastapi import status
from fastapi.responses import JSONResponse

from app.crud.dependencies import validate_submenu_model
from app.crud.dish import DishCRUDService, get_dish_service
from app.db.models import Dish, DishCreate, DishUpdate, Menu

router = APIRouter()


@router.get("/", response_model=list[Dish])
async def list_dish(
    crud_service: DishCRUDService = Depends(get_dish_service),
    submenu: Menu = Depends(validate_submenu_model),
) -> List[Dish]:
    return await crud_service.list(submenu_id=submenu.id)


@router.get("/{item_id}", response_model=Dish)
async def get_dish(
    item_id: UUID4,
    crud_service: DishCRUDService = Depends(get_dish_service),
) -> Optional[Dish]:
    return await crud_service.get(item_id)


@router.post("/", response_model=Dish, status_code=status.HTTP_201_CREATED)
async def add_dish(
    item_create: DishCreate,
    crud_service: DishCRUDService = Depends(get_dish_service),
    submenu: Menu = Depends(validate_submenu_model),
) -> Optional[Dish]:
    return await crud_service.create(item_create, submenu_id=submenu.id)


@router.patch("/{item_id}", response_model=Dish)
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
