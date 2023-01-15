from fastapi import APIRouter, Depends

from .dependencies import validate_menu_model, validate_submenu_model
from .endpoints import menu, submenu, dish

router = APIRouter()
router.include_router(menu.router, prefix="/menus", tags=["Menus"])
router.include_router(
    submenu.router,
    prefix="/menus/{menu_id}/submenus",
    tags=["Submenus"],
    dependencies=[Depends(validate_menu_model)],
)
router.include_router(
    dish.router,
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"],
    dependencies=[Depends(validate_menu_model), Depends(validate_submenu_model)],
)