from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.core.load_random_users import loader_random_users

from app.database import setup_database
from app.routers.api.v1.users import router as user_router
from app.config import Settings
from app.routers.ssr.pages import router as pages_router

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Загрузка"""
    await setup_database()
    await loader_random_users()
    yield


app = FastAPI(
    title="YADRO WEB TEST",
    description="Тестовое задание от команды разработки внутренних продуктов - Команда разработки внутренних продуктов",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(pages_router, prefix="")
app.include_router(user_router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host=settings.host, port=settings.port)
