from typing import Optional

from fastapi import Depends, Request

from app.crud.menu import MenuCRUDService, get_menu_service
from app.crud.submenu import SubmenuCRUDService, get_submenu_service
from app.db.models import Menu


async def validate_menu_model(
    request: Request,
    crud_service: MenuCRUDService = Depends(get_menu_service),
) -> Optional[Menu]:
    """
    The validate_menu_model function is a dependency function that will be used
    by the get_menu_by_id endpoint. It takes in a request object and returns an
    instance of MenuModel. It does this by using the get method from
    MenuCRUDService class to retrieve an instance of MenuModel from database.
    """
    menu_id = request.path_params.get("menu_id")
    return await crud_service.get(menu_id)


async def validate_submenu_model(
    request: Request,
    crud_service: SubmenuCRUDService = Depends(get_submenu_service),
):
    """
    The validate_submenu_model function is a dependency function that will be
    used by the create_submenu and update_submenu functions. It takes in a
    request object, which contains the path parameters of the submenu id, and
    returns an instance of Submenu model if it exists.
    """
    menu_id = request.path_params.get("submenu_id")
    return await crud_service.get(menu_id)


async def get_submenu_id(
    request: Request,
):
    """
    The get_submenu_id function is a dependency function that gets and return
    submenu_id from Request.
    """
    return request.path_params.get("submenu_id")
