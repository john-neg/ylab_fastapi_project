import os.path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import ExcelStyle, settings
from app.db.database import get_session
from app.db.models import TaskDataResponse
from app.services.reports import get_menus_report_data
from app.tasks.tasks import generate_menu_xlsx, get_task_info

router = APIRouter()


@router.post(
    "/menus",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TaskDataResponse,
    summary="Сформировать Excel файл меню",
)
async def generate_menus_report(
    db_session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    menus_data = await get_menus_report_data(db_session)
    task_id = generate_menu_xlsx.delay(menus_data)
    return JSONResponse(
        content=get_task_info(task_id), status_code=status.HTTP_202_ACCEPTED
    )


@router.get(
    "/menus/{task_id}",
    summary="Скачать Excel файл меню",
    responses={status.HTTP_425_TOO_EARLY: {"model": TaskDataResponse}},
)
async def get_menus_report(task_id: str) -> FileResponse:
    task_data = get_task_info(task_id)
    if task_data.get("task_result"):
        path = os.path.join(settings.FILES_DIR, f"{task_id}.xlsx")
        return FileResponse(
            path=path,
            filename="Menu.xlsx",
            media_type=ExcelStyle.FileType,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_425_TOO_EARLY,
            detail=task_data,
        )
