from fastapi import FastAPI

from app.api.api_v1.endpoints import menu
from app.core.config import Settings


settings = Settings()
app = FastAPI(docs_url="/")

app.include_router(menu.router, prefix="/api/v1")
