import asyncio
import uvicorn
from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.core.load_random_users import loader_random_users

from app.database import setup_database
from app.routers.api.v1.users import router as user_router
from app.routers.ssr.pages import router as pages_router
from app.config import settings

async def init_database():
    """Загрузка"""
    await setup_database()
    await loader_random_users()


app = FastAPI(
    title="YADRO WEB TEST",
    description="Тестовое задание от команды разработки внутренних продуктов - Команда разработки внутренних продуктов",
    version="1.0.0",
)

app.include_router(pages_router, prefix="")
app.include_router(user_router, prefix="/api/v1")

app.mount("/static", StaticFiles(directory="app/static"), name="static")


async def main():
    await init_database()
    if settings.debug:
        uvicorn.run("app.main:app", host=settings.host, reload=True)
    else:
        uvicorn.run("app.main:app", host=settings.host, workers=4)


if __name__ == "__main__":
    asyncio.run(main())