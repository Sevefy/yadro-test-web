import random
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import SessionDep
from app.repository.users import UserRepository
from app.routers.api.v1.pagination import pagination_parameters
from app.routers.api.v1.users import router as user_router
from app.config import logger

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
async def get_index_page(request: Request, session: SessionDep, pagination: dict = Depends(pagination_parameters)):
    limit, offset = pagination["limit"], pagination["offset"]
    total_users = await UserRepository.get_total_users(session)
    if not total_users:
        raise HTTPException(status_code=400, detail="Нет пользователей")
    users = await UserRepository.get_all_users(session, limit, offset)
    
    current_page = (offset // limit) + 1 if limit > 0 else 1
    total_pages = (total_users + limit - 1) // limit if limit > 0 else 1
    
    return templates.TemplateResponse(
        request=request, name="index.html", 
        context={
            "users": users,
            "limit": limit,
            "offset": offset,
            "current_page": current_page,
            "total_pages": total_pages,
            "total_users": total_users
        }
    )


@app.get("/random", response_class=HTMLResponse)
async def get_random_user_page(request: Request, session: SessionDep):
    total_users = await UserRepository.get_total_users(session)
    if not total_users:
        raise HTTPException(status_code=400, detail="Нет пользователей")
    user_id = random.randint(1, total_users)
    user = await UserRepository.get_user_by_id(session, user_id)
    return templates.TemplateResponse(
        request=request, name="random_user.html", context={"user": user}
    )

@app.get("/{user_id}", response_class=HTMLResponse)
async def get_concrete_user_page(request: Request, session: SessionDep, user_id: int):
    try:
        user = await UserRepository.get_user_by_id(session, user_id)
        return templates.TemplateResponse(
            request=request, name="concrete_user.html", context={"user": user}
        )
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={user_id} не найден")


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
