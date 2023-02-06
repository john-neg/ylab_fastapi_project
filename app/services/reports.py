from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models import Menu
from app.services.menu import MenuModelService


async def get_menus_report_data(db_session: AsyncSession) -> list[dict]:
    """
    The get_menus_report_data function returns a json compatible list of
    dictionaries, related to Menu, Submenu and Dish models data.
    """
    db_service = MenuModelService(Menu, db_session)
    menus_list = await db_service.list()
    menus_report_data = [
        {
            "title": menu.title,
            "description": menu.description,
            "submenus": [
                {
                    "title": submenu.title,
                    "description": submenu.description,
                    "dishes": [
                        {
                            "title": dish.title,
                            "description": dish.description,
                            "price": str(dish.price),
                        }
                        for dish in submenu.dishes
                    ],
                }
                for submenu in menu.submenus
            ],
        }
        for menu in menus_list
    ]
    return menus_report_data
