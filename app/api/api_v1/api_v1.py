from fastapi import APIRouter

from app.api.api_v1.endpoints import dish, menu, submenu

router = APIRouter()
router.include_router(menu.router, prefix="/menus", tags=["Menus"])
router.include_router(
    submenu.router,
    prefix="/menus/{menu_id}/submenus",
    tags=["Submenus"],
)
router.include_router(
    dish.router,
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes",
    tags=["Dishes"],
)
