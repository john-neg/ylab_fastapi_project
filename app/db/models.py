import asyncio
import uuid
from typing import Optional, List, Any

from fastapi import Depends
from pydantic.types import UUID4, condecimal
from sqlalchemy.ext.hybrid import hybrid_property
from sqlmodel import column
from sqlmodel import func
from sqlalchemy.orm import column_property, declared_attr
from sqlmodel import SQLModel, Field, Relationship, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import get_session


class DefaultBase(SQLModel):
    """Base class for menus and dishes."""

    pass


class DefaultUUIDBase(DefaultBase):
    """Base UUID class for menus and dishes."""

    id: UUID4 = Field(
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default_factory=uuid.uuid4,
    )


class DefaultModelBase(DefaultBase):
    """Base model class for menus and dishes."""

    title: str
    description: str


class DefaultCreateBase(DefaultModelBase):
    """Base create class for menus and dishes."""

    pass


class DefaultReadBase(DefaultUUIDBase, DefaultModelBase):
    """Base read class for menus and dishes."""

    pass


class DefaultUpdateBase(DefaultBase):
    """Base update class for menus and dishes."""

    title: Optional[str]
    description: Optional[str]


class Menu(DefaultUUIDBase, DefaultModelBase, table=True):
    """Menu model class."""

    submenus: List["Submenu"] = Relationship(
        back_populates="menu",
        sa_relationship_kwargs={"cascade": "all,delete", 'lazy': 'selectin'},
    )


class MenuCreate(DefaultCreateBase):
    """Menu create class."""

    pass


class MenuRead(DefaultReadBase):
    """Base read class for menus and dishes."""

    # submenus_count: int
    pass


class MenuUpdate(DefaultUpdateBase):
    """Menu update class."""

    pass


class Submenu(DefaultUUIDBase, DefaultModelBase, table=True):
    """Submenu model class."""

    def __init__(self, dishes_count: int, **data: Any):
        super().__init__(**data)
        self._dishes_count = dishes_count

    menu_id: UUID4 = Field(foreign_key="menu.id", nullable=False, index=True)
    menu: Menu = Relationship(back_populates="submenus")
    dishes: list["Dish"] = Relationship(
        back_populates="submenu",
        sa_relationship_kwargs={"cascade": "all,delete", 'lazy': 'selectin'},
    )

    @hybrid_property
    def dishes_count(self):
        return self._dishes_count

    @dishes_count.setter
    async def set_attrib(self, dishes_count):
        await asyncio.sleep(1.0)
        self._dishes_count = dishes_count

    # async def count_submenus(self, menu_id) -> int:
    #     result = await self.db_session.scalar(
    #         select(func.count(Submenu.id)).where(
    #             Submenu.menu_id == menu_id,
    #         )
    #     )
    #     return result
    #
    # async def count_dishes(self, menu_id, submenu_id) -> int:
    #     result = await self.db_session.scalar(
    #         select(func.count(Dish.id)).where(
    #             Submenu.menu_id == menu_id,
    #             Dish.submenu_id == submenu_id,
    #         )
    #     )
    #     return result


class SubmenuCreate(DefaultCreateBase):
    """Submenu create class."""

    pass


class SubmenuRead(DefaultReadBase):
    """Submenu read class."""

    dishes_count: int = Field(alias="dishes_count")


class SubmenuUpdate(DefaultUpdateBase):
    """Submenu update class."""

    pass


class Dish(DefaultUUIDBase, DefaultModelBase, table=True):
    """Dish model class."""

    price: condecimal(decimal_places=2) = Field(default=None)
    submenu_id: UUID4 = Field(
        foreign_key="submenu.id",
        nullable=False,
        index=True,
    )
    submenu: Submenu = Relationship(back_populates="dishes")


class DishCreate(DefaultCreateBase):
    """Dish create class."""

    price: condecimal(decimal_places=2)


class DishRead(DefaultReadBase):
    """Dish read class."""

    pass


class DishUpdate(DefaultUpdateBase):
    """Dish update class."""

    price: Optional[condecimal(decimal_places=2)]
