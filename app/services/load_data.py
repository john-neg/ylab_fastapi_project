import json
import os

from app.core.config import BASEDIR
from app.db.models import DishCreate, MenuCreate, SubmenuCreate
from app.services.dish import DishCRUDService
from app.services.menu import MenuCRUDService
from app.services.submenu import SubmenuCRUDService


async def load_json_data(
    menu_service: MenuCRUDService,
    submenu_service: SubmenuCRUDService,
    dish_service: DishCRUDService,
) -> None:
    """
    The load_json_data function is used to load the initial data into the
    database.
    """
    path = os.path.join(BASEDIR, "app/db/data/db_data.json")
    with open(path) as file:
        load_data = json.loads(file.read())
        for menu in load_data:
            menu_obj = await menu_service.create(
                MenuCreate(
                    title=menu.get("title"),
                    description=menu.get("description"),
                )
            )
            menu_id = menu_obj.id
            for submenu in menu.get("submenus"):
                submenu_obj = await submenu_service.create(
                    SubmenuCreate(
                        title=submenu.get("title"),
                        description=submenu.get("description"),
                    ),
                    menu_id=menu_id,
                )
                submenu_id = submenu_obj.id
                for dish in submenu.get("dishes"):
                    await dish_service.create(
                        DishCreate(
                            title=dish.get("title"),
                            description=dish.get("description"),
                            price=dish.get("price"),
                        ),
                        submenu_id=submenu_id,
                    )
