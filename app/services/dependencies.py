from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import get_session
from app.db.models import Menu, Submenu
from app.services.menu import MenuModelService
from app.services.submenu import SubmenuModelService


async def validate_menu_model(
    request: Request,
    db_session: AsyncSession = Depends(get_session),
) -> Menu | None:
    """
    The validate_menu_model function is a dependency function that will be used
    by the get_menu_by_id endpoint. It takes in a request object and returns an
    instance of MenuModel. It does this by using the get method from
    MenuCRUDService class to retrieve an instance of MenuModel from database.
    """
    menu_id = request.path_params.get('menu_id')
    db_service = MenuModelService(Menu, db_session)
    return await db_service.get(menu_id)


async def validate_submenu_model(
    request: Request,
    db_session: AsyncSession = Depends(get_session),
):
    """
    The validate_submenu_model function is a dependency function that takes in
    the request object and db_session object. It then uses the path parameters
    to get the submenu id from the url. The submenu id is used to query
    the database for a specific menu item using SubmenuModelService.
    This function will be used as a dependency in other functions.
    """
    menu_id = request.path_params.get('submenu_id')
    db_service = SubmenuModelService(Submenu, db_session)
    return await db_service.get(menu_id)


async def get_submenu_id(
    request: Request,
):
    """
    The get_submenu_id function is a dependency function that gets and return
    submenu_id from Request.
    """
    return request.path_params.get('submenu_id')
