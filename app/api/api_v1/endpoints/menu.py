from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic.types import UUID4

from app.services.menu import MenuCRUDService, get_menu_service
from app.db.models import MenuCreate, MenuRead, MenuUpdate

router = APIRouter()


@router.get("/", response_model=list[MenuRead])
async def list_menu(
    service: MenuCRUDService = Depends(get_menu_service),
) -> list[dict[str, int]]:
    return await service.list()


@router.get("/{menu_id}", response_model=MenuRead)
async def get_menu(
    menu_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> dict[str, int]:
    return await crud_service.get(menu_id)


@router.post("/", response_model=MenuRead, status_code=status.HTTP_201_CREATED)
async def add_menu(
    item_create: MenuCreate,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> dict[str, int]:
    update = await crud_service.create(item_create)
    return await crud_service.get(update.id)


@router.patch("/{menu_id}", response_model=MenuRead)
async def update_menu(
    menu_id: UUID4,
    item_update: MenuUpdate,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> dict[str, int]:
    return await crud_service.update(menu_id, item_update)


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> JSONResponse:
    return await crud_service.delete(menu_id)
