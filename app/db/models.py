import uuid
from typing import Optional, List

from pydantic.types import UUID4, condecimal
from sqlmodel import SQLModel, Field, Relationship


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

    menu_id: UUID4 = Field(foreign_key="menu.id", nullable=False, index=True)
    menu: Menu = Relationship(back_populates="submenus")
    dishes: List["Dish"] = Relationship(
        back_populates="submenu",
        sa_relationship_kwargs={"cascade": "all,delete", 'lazy': 'selectin'},
    )
    # dishes_count: int


class SubmenuCreate(DefaultCreateBase):
    """Submenu create class."""

    pass


class SubmenuRead(DefaultReadBase):
    """Submenu read class."""

    # dishes_count: int


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
