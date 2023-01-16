from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic.types import UUID4

from app.crud.dependencies import validate_menu_model
from app.crud.submenu import SubmenuCRUDService, get_submenu_service
from app.db.models import Menu, SubmenuCreate, SubmenuRead, SubmenuUpdate

router = APIRouter()


async def response_builder(submenu):
    """
    The response_builder function takes a submenu and its id as input,
    and returns the submenu with an added field dishes_count.
    The dishes_count is the number of dishes in that particular submenu.
    """
    return {
        **submenu.dict(),
        "dishes_count": submenu.dishes.__len__(),
    }


@router.get("/", response_model=list[SubmenuRead])
async def list_submenu(
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
    menu: Menu = Depends(validate_menu_model),
) -> list[dict[str, int]]:
    return [
        await response_builder(submenu)
        for submenu in await crud_service.list(menu_id=menu.id)
    ]


@router.get("/{item_id}", response_model=SubmenuRead)
async def get_submenu(
    item_id: UUID4,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
) -> dict[str, int]:
    submenu = await crud_service.get(item_id)
    return await response_builder(submenu)


@router.post(
    "/", response_model=SubmenuRead, status_code=status.HTTP_201_CREATED
)
async def add_submenu(
    item_create: SubmenuCreate,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
    menu: Menu = Depends(validate_menu_model),
) -> dict[str, int]:
    submenu = await crud_service.create(item_create, menu_id=menu.id)
    return await response_builder(submenu)


@router.patch("/{item_id}", response_model=SubmenuRead)
async def update_submenu(
    item_id: UUID4,
    item_update: SubmenuUpdate,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
) -> dict[str, int]:
    submenu = await crud_service.update(item_id, item_update)
    return await response_builder(submenu)


@router.delete("/{item_id}")
async def delete_submenu(
    item_id: UUID4,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
) -> JSONResponse:
    return await crud_service.delete(item_id)
