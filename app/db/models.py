import uuid
from typing import Optional, List

from pydantic.types import UUID4, condecimal
from sqlmodel import SQLModel, Field, Relationship


class DefaultBase(SQLModel):
    """Base class for menus and dishes."""

    title: str
    description: str


class DefaultModelBase(DefaultBase):
    """Base model class for menus and dishes."""

    id: UUID4 = Field(
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default_factory=uuid.uuid4,
    )
    pass


class DefaultCreateBase(DefaultBase):
    """Base create class for menus and dishes."""

    pass


class DefaultReadBase(DefaultBase):
    """Base read class for menus and dishes."""

    pass


class DefaultUpdateBase(SQLModel):
    """Base update class for menus and dishes."""

    title: Optional[str]
    description: Optional[str]


class Menu(DefaultModelBase, table=True):
    """Menu model class."""

    submenus: List["Submenu"] = Relationship(
        back_populates="menu",
        sa_relationship_kwargs={"cascade": "all,delete"},
    )


class MenuCreate(DefaultCreateBase):
    """Menu create class."""

    pass


class MenuUpdate(DefaultUpdateBase):
    """Menu update class."""

    pass


class Submenu(DefaultModelBase, table=True):
    """Submenu model class."""

    menu_id: UUID4 = Field(foreign_key="menu.id", nullable=False, index=True)
    menu: Menu = Relationship(
        back_populates="submenus"
    )
    dishes: List["Dish"] = Relationship(
        back_populates="submenu",
        sa_relationship_kwargs={"cascade": "all,delete"},
    )


class SubmenuCreate(DefaultCreateBase):
    """Submenu create class."""

    pass


class SubmenuUpdate(DefaultUpdateBase):
    """Submenu update class."""

    pass


class Dish(DefaultModelBase, table=True):
    """Dish model class."""

    price: condecimal(decimal_places=2) = Field(default=None)
    submenu_id: UUID4 = Field(foreign_key="submenu.id", nullable=False, index=True)
    submenu: Submenu = Relationship(
        back_populates="dishes"
    )


class DishCreate(DefaultCreateBase):
    """Dish create class."""

    price: condecimal(decimal_places=2)


class DishUpdate(DefaultUpdateBase):
    """Dish update class."""

    price: Optional[condecimal(decimal_places=2)]
