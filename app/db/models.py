import uuid
from typing import Optional

from pydantic.types import UUID4
from sqlmodel import SQLModel, Field


class DefaultBase(SQLModel):
    """Base class for menus and dishes."""

    title: str
    description: str


class DefaultCreateBase(DefaultBase):
    """Base create class for menus and dishes."""

    pass


class DefaultUpdateBase(SQLModel):
    """Base update class for menus and dishes."""

    title: Optional[str]
    description: Optional[str]


class Menu(DefaultBase, table=True):
    """Menu model class."""

    id: UUID4 = Field(
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default_factory=uuid.uuid4,
    )


class MenuCreate(DefaultCreateBase):
    """Menu create class."""

    pass


class MenuUpdate(DefaultUpdateBase):
    """Menu update class."""

    pass
