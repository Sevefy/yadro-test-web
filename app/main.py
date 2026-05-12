import random
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import SessionDep
from app.repository.users import UserRepository
from app.routers.api.v1.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Загрузка"""
    # await setup_database()
    # await loader_random_users()
    yield


app = FastAPI(
    title="YADRO WEB TEST",
    description="Тестовое задание от команды разработки внутренних продуктов - Команда разработки внутренних продуктов",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(user_router, prefix="/api/v1")


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_index_page(request: Request, session: SessionDep):
    users = await UserRepository.get_all_users(session)
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/random", response_class=HTMLResponse)
async def get_random_user_page(request: Request, session: SessionDep):
    user_id = random.randint(1, 1000)
    user = await UserRepository.get_user_by_id(session, user_id)
    return templates.TemplateResponse(
        request=request, name="random_user.html", context={"id": user.id}
    )

@app.get("/{user_id}", response_class=HTMLResponse)
async def get_concrete_user_page(request: Request, session: SessionDep, user_id: int):
    user = await UserRepository.get_user_by_id(session, user_id)
    return templates.TemplateResponse(
        request=request, name="concrete_user.html", context={"id": user.id}
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
