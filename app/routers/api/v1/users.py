import random
from typing import List

from fastapi import APIRouter, Depends

from app.database import SessionDep
from app.repository.users import UserRepository
from app.schemas.users import UserSchemaResponse

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

def pagination_parameters(limit: int = 50, offset: int = 0):
    return {
        "limit": limit,
        "offset": offset
    }


@router.get(path="", status_code=200)
async def get_users(session: SessionDep, pagination: dict = Depends(pagination_parameters)) -> List[UserSchemaResponse]:
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
    user_id = random.randint(1, 1000)
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
    
