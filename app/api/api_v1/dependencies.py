from fastapi import Request, Depends

from .services.menu import MenuCRUDService, get_menu_service
from .services.submenu import SubmenuCRUDService, get_submenu_service


async def validate_menu_model(
    request: Request,
    crud_service: MenuCRUDService = Depends(get_menu_service),
):
    menu_id = request.path_params.get("menu_id")
    return await crud_service.get(menu_id)


async def validate_submenu_model(
    request: Request,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
):
    menu_id = request.path_params.get("submenu_id")
    return await crud_service.get(menu_id)
