import random

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.database import SessionDep
from app.repository.users import UserRepository
from app.schemas.users import UserSchemaResponse
from app.routers.api.v1.pagination import paginationDep
   
router = APIRouter(prefix="", tags=["Страницы"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_index_page(request: Request, session: SessionDep, pagination: paginationDep):
    limit, offset = pagination["limit"], pagination["offset"]
    total_users = await UserRepository.get_total_users(session)
    if not total_users:
        raise HTTPException(status_code=400, detail="Нет пользователей")
    isntances = await UserRepository.get_all_users(session, limit, offset)
    users = [
        UserSchemaResponse(
            first_name=instance.first_name,
            last_name=instance.last_name,
            gender=instance.gender,
            phone=instance.phone,
            email=instance.email,
            address=instance.address,
            links={"self": f"http://localhost:8000/{instance.id}"},
        )
        for instance in isntances
    ]
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


@router.get("/random", response_class=HTMLResponse)
async def get_random_user_page(request: Request, session: SessionDep):
    total_users = await UserRepository.get_total_users(session)
    if not total_users:
        raise HTTPException(status_code=400, detail="Нет пользователей")
    user_id = random.randint(1, total_users)
    instance = await UserRepository.get_user_by_id(session, user_id)
    user = UserSchemaResponse(
        first_name=instance.first_name,
        last_name=instance.last_name,
        gender=instance.gender,
        phone=instance.phone,
        email=instance.email,
        address=instance.address,
        links={"all": "http://localhost:8000"},
    )
    return templates.TemplateResponse(
        request=request, name="concrete_user.html", context={"user": user}
    )

@router.get("/{user_id}", response_class=HTMLResponse)
async def get_concrete_user_page(request: Request, session: SessionDep, user_id: int):
    try:
        instance = await UserRepository.get_user_by_id(session, user_id)
        user = UserSchemaResponse(
            first_name=instance.first_name,
            last_name=instance.last_name,
            gender=instance.gender,
            phone=instance.phone,
            email=instance.email,
            address=instance.address,
            links={"all": "http://localhost:8000"}
        )
        return templates.TemplateResponse(
            request=request, name="concrete_user.html", context={"user": user}
        )
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={user_id} не найден")
