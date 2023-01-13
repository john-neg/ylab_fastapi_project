from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.db.models import Menu, MenuCreate


router = APIRouter(
    prefix="/menus",
    tags=["menus"],
    responses={404: {"detail": "menu not found"}},
)


@router.get("/", response_model=list[Menu])
async def get_menus(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Menu))
    songs = result.scalars().all()
    return [
        Menu(title=menu.title, description=menu.description, id=menu.id)
        for menu in songs
    ]


@router.post("/")
async def add_menu(menu: MenuCreate, session: AsyncSession = Depends(get_session)):
    menu = Menu(title=menu.title, description=menu.description)
    session.add(menu)
    await session.commit()
    await session.refresh(menu)
    return menu
