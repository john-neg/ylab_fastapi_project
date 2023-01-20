from typing import AsyncGenerator, Callable, List

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.pool import StaticPool

from app.db.models import Menu


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as ac:
        yield ac


@pytest.fixture(scope="function")
def override_get_session(session: AsyncSession) -> Callable:
    async def _override_get_session():
        yield session

    return _override_get_session


@pytest.fixture(scope="function")
def app(override_get_session: Callable) -> FastAPI:

    from app.db.database import get_session

    from app.main import app

    app.dependency_overrides[get_session] = override_get_session
    return app


@pytest.fixture(scope="function")
async def create_and_get_menus(session: AsyncSession) -> List[str]:
    list_menu_name = ["menu1", "menu2"]
    menu = [
        Menu(
            title=name_tag, description=f"Description {name_tag}"
        ) for name_tag in list_menu_name
    ]
    session.add_all(menu)
    await session.commit()
    yield list_menu_name
    await session.rollback()
