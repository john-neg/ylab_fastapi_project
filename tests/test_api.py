import pytest
from httpx import AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.models import Dish, Menu, Submenu
from tests.base import BaseApiCRUDTests


@pytest.mark.asyncio
class TestMenu(BaseApiCRUDTests):
    url: str = f"{settings.API_V1_STR}/menus/"
    name: str = "menu"
    required_fields: tuple = ("title", "description")
    db_table = Menu

    async def test_delete_nested_objects(
        self,
        async_client: AsyncClient,
        test_session: AsyncSession,
        initial_db_data: dict,
    ):
        """Test that nested Submenu objects deletes after DELETE request."""
        item_id = initial_db_data[f"check_{self.name}"][f"{self.name}1"]["id"]

        statement = select(Submenu).where(Submenu.menu_id == item_id)
        results = await test_session.execute(statement=statement)
        assert (
            len(results.all()) > 0
        ), "Check that initial_db_data contains nested objects"

        response = await async_client.delete(f"{self.url}{item_id}")
        assert (
            response.status_code == 200
        ), f"Check that DELETE request to {self.url} returns 200 code"

        statement = select(Submenu).where(Submenu.menu_id == item_id)
        results = await test_session.execute(statement=statement)
        assert (
            len(results.all()) == 0
        ), "Check that DELETE request deletes nested objects"


@pytest.mark.asyncio
class TestSubmenu(BaseApiCRUDTests):
    menu_id: str = "f47d47e4-efb5-4700-8147-ddcc5987b1fc"
    url: str = f"{settings.API_V1_STR}/menus/{menu_id}/submenus/"
    name: str = "submenu"
    required_fields: tuple = ("title", "description")
    db_table = Submenu

    async def test_delete_nested_objects(
        self,
        async_client: AsyncClient,
        test_session: AsyncSession,
        initial_db_data: dict,
    ):
        """Test that nested Dish objects deletes after DELETE request."""
        item_id = initial_db_data[f"check_{self.name}"][f"{self.name}1"]["id"]

        statement = select(Dish).where(Dish.submenu_id == item_id)
        results = await test_session.execute(statement=statement)
        assert (
            len(results.all()) > 0
        ), "Check that initial_db_data contains nested objects"

        response = await async_client.delete(f"{self.url}{item_id}")
        assert (
            response.status_code == 200
        ), f"Check that DELETE request to {self.url} returns 200 code"

        statement = select(Dish).where(Dish.submenu_id == item_id)
        results = await test_session.execute(statement=statement)
        assert (
            len(results.all()) == 0
        ), "Check that DELETE request deletes nested objects"


@pytest.mark.asyncio
class TestDish(BaseApiCRUDTests):
    menu_id: str = "f47d47e4-efb5-4700-8147-ddcc5987b1fc"
    submenu_id: str = "127c9770-456c-478d-a086-e8e313e64d68"
    url: str = f"{settings.API_V1_STR}/menus/{menu_id}/submenus/{submenu_id}/dishes/"
    name: str = "dish"
    required_fields: tuple = ("title", "description", "price")
    db_table = Dish
