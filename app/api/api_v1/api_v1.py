from fastapi import APIRouter

from app.api.api_v1.endpoints import menu

router = APIRouter()
router.include_router(menu.router, prefix="/menus", tags=["menus"])
