from fastapi import FastAPI

from app.api.api_v1 import api_v1
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, docs_url="/")

app.include_router(api_v1.router, prefix=settings.API_V1_STR)
