from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.services.dish import DishCRUDService, get_dish_service
from app.services.load_data import load_json_data
from app.services.menu import MenuCRUDService, get_menu_service
from app.services.submenu import SubmenuCRUDService, get_submenu_service

router = APIRouter()


@router.post(
    "/",
    summary="Загрузить тестовые данные",
    status_code=status.HTTP_201_CREATED,
)
async def load_data(
    menu_service: MenuCRUDService = Depends(get_menu_service),
    submenu_service: SubmenuCRUDService = Depends(get_submenu_service),
    dish_service: DishCRUDService = Depends(get_dish_service),
) -> JSONResponse:
    await load_json_data(menu_service, submenu_service, dish_service)
    response_data = {"message": "Test DB data loaded"}
    return JSONResponse(
        content=response_data,
        status_code=status.HTTP_201_CREATED,
    )
