from fastapi import FastAPI

from app.api.api_v1 import api_v1
from app.core.config import Settings


settings = Settings()
app = FastAPI(docs_url="/")

app.include_router(api_v1.router, prefix="/api/v1")
