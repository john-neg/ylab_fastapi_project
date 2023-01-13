import uuid

from pydantic.types import UUID4
from sqlmodel import SQLModel, Field


class DefaultBase(SQLModel):
    """Base mixin class for menus and dishes."""

    title: str
    description: str


class Menu(DefaultBase, table=True):
    """Menu model class."""

    id: UUID4 = Field(
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        default_factory=uuid.uuid4,
    )


class MenuCreate(DefaultBase):
    """Menu create class."""

    pass
