import uuid

from pydantic.types import UUID4, condecimal
from sqlmodel import Field, Relationship, SQLModel


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

    title: str | None
    description: str | None


class Menu(DefaultUUIDBase, DefaultModelBase, table=True):
    """Menu model class."""

    submenus: list['Submenu'] = Relationship(
        back_populates='menu',
        sa_relationship_kwargs={'cascade': 'all,delete', 'lazy': 'selectin'},
    )


class MenuCreate(DefaultCreateBase):
    """Menu create class."""

    class Config:
        schema_extra = {
            'example': {
                'title': 'My menu',
                'description': 'My menu description',
            },
        }


class MenuRead(DefaultReadBase):
    """Base read class for menus and dishes."""

    submenus_count: int
    dishes_count: int


class MenuUpdate(DefaultUpdateBase):
    """Menu update class."""

    class Config:
        schema_extra = {
            'example': {
                'title': 'My updated menu',
                'description': 'My updated menu description',
            },
        }


class Submenu(DefaultUUIDBase, DefaultModelBase, table=True):
    """Submenu model class."""

    menu_id: UUID4 = Field(foreign_key='menu.id', nullable=False, index=True)
    menu: Menu = Relationship(back_populates='submenus')
    dishes: list['Dish'] = Relationship(
        back_populates='submenu',
        sa_relationship_kwargs={'cascade': 'all,delete', 'lazy': 'selectin'},
    )


class SubmenuCreate(DefaultCreateBase):
    """Submenu create class."""

    class Config:
        schema_extra = {
            'example': {
                'title': 'My submenu',
                'description': 'My submenu description',
            },
        }


class SubmenuRead(DefaultReadBase):
    """Submenu read class."""

    dishes_count: int


class SubmenuUpdate(DefaultUpdateBase):
    """Submenu update class."""

    class Config:
        schema_extra = {
            'example': {
                'title': 'My updated submenu',
                'description': 'My updated submenu description',
            },
        }


class Dish(DefaultUUIDBase, DefaultModelBase, table=True):
    """Dish model class."""

    price: condecimal(decimal_places=2) = Field(default=None)
    submenu_id: UUID4 = Field(
        foreign_key='submenu.id',
        nullable=False,
        index=True,
    )
    submenu: Submenu = Relationship(back_populates='dishes')


class DishCreate(DefaultCreateBase):
    """Dish create class."""

    price: condecimal(decimal_places=2)

    class Config:
        schema_extra = {
            'example': {
                'title': 'My dish',
                'description': 'My dish description',
            },
        }


class DishRead(DefaultReadBase):
    """Dish read class."""

    price: str


class DishUpdate(DefaultUpdateBase):
    """Dish update class."""

    price: condecimal(decimal_places=2) | None

    class Config:
        schema_extra = {
            'example': {
                'title': 'My updated dish',
                'description': 'My updated dish description',
                'price': '10.50',
            },
        }
