from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic.types import UUID4

from app.crud.menu import MenuCRUDService, get_menu_service
from app.db.models import MenuCreate, MenuRead, MenuUpdate

router = APIRouter()


async def response_builder(menu):
    """
    The response_builder function takes a menu object and returns a dictionary
    containing the menu's data. It also includes the number of submenus and
    dishes associated with that menu.
    """
    return {
        **menu.dict(),
        "submenus_count": len(menu.submenus),
        "dishes_count": sum(
            [len(submenu.dishes) for submenu in menu.submenus]
        )
    }


@router.get("/", response_model=list[MenuRead])
async def list_menu(
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> list[dict[str, int]]:
    return [await response_builder(menu) for menu in await crud_service.list()]


@router.get("/{menu_id}", response_model=MenuRead)
async def get_menu(
    menu_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> dict[str, int]:
    menu = await crud_service.get(menu_id)
    return await response_builder(menu)


@router.post("/", response_model=MenuRead, status_code=status.HTTP_201_CREATED)
async def add_menu(
    item_create: MenuCreate,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> dict[str, int]:
    update = await crud_service.create(item_create)
    menu = await crud_service.get(update.id)
    return await response_builder(menu)


@router.patch("/{menu_id}", response_model=MenuRead)
async def update_menu(
    menu_id: UUID4,
    item_update: MenuUpdate,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> dict[str, int]:
    menu = await crud_service.update(menu_id, item_update)
    return await response_builder(menu)


@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: UUID4,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> JSONResponse:
    return await crud_service.delete(menu_id)
