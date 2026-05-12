import random
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.database import SessionDep
from app.repository.users import UserRepository
from app.routers.api.v1.pagination import paginationDep
from app.schemas.users import UserSchemaResponse

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router.get(path="", status_code=200)
async def get_users(session: SessionDep, pagination: paginationDep) -> List[UserSchemaResponse]:
    offset, limit = pagination["offset"], pagination["limit"]
    users = await UserRepository.get_all_users(session, limit, offset)
    result = [
        UserSchemaResponse(
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender,
            phone=user.phone,
            email=user.email,
            address=user.address,
            links=[
                {"self": f"http://localhost:8000/api/v1{router.prefix}/{user.id}"},
            ]
        )
        for user in users
    ]
    return result


@router.get(path="/random", status_code=200)
async def get_random_user(session: SessionDep) -> UserSchemaResponse:
    total_users = await UserRepository.get_total_users(session)
    if not total_users:
        raise HTTPException(status_code=400, detail="Нет пользователей")
    user_id = random.randint(1, total_users)
    user = await UserRepository.get_user_by_id(session, user_id)
    return  UserSchemaResponse(
            first_name=user.first_name,
            last_name=user.last_name,
            gender=user.gender,
            phone=user.phone,
            email=user.email,
            address=user.address,
            links=[
                {"all": "http://localhost:8000/api/v1/users"}
            ]
        )

@router.get(path="/{user_id}", status_code=200)
async def get_concrete_user(session: SessionDep, user_id:int) -> UserSchemaResponse:
    try:
        user = await UserRepository.get_user_by_id(session, user_id)
        return  UserSchemaResponse(
                first_name=user.first_name,
                last_name=user.last_name,
                gender=user.gender,
                phone=user.phone,
                email=user.email,
                address=user.address,
                links=[
                    {"all": "http://localhost:8000/api/v1/users"}
                ]
            )
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={user_id} не найден")
    
