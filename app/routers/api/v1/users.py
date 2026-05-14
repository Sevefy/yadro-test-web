from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.load_random_users import loader_random_users
from app.database import SessionDep
from app.repository.users import UserRepository
from app.routers.api.v1.pagination import paginationDep
from app.schemas.users import LoadNewUsers, UserSchemaResponse
from fastapi import BackgroundTasks
from app.config import logger
router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router.get(path="", status_code=200)
async def get_users(request: Request, session: SessionDep, pagination: paginationDep) -> list[UserSchemaResponse]:
    base_url = str(request.base_url).rstrip('/')
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
            links={"self": f"{base_url}/api/v1{router.prefix}/{user.id}"},
        )
        for user in users
    ]
    return result


@router.get(path="/random", status_code=200)
async def get_random_user(request: Request, session: SessionDep) -> UserSchemaResponse:
    base_url = str(request.base_url).rstrip('/')
    try:
        instance = await UserRepository.get_random_user(session)
    except ValueError:
        raise HTTPException(status_code=404, detail="Нет пользователей")
    except Exception as e:
        logger.error(f"Server Error: {e}")
        raise HTTPException(status_code=500)
    return  UserSchemaResponse(
            first_name=instance.first_name,
            last_name=instance.last_name,
            gender=instance.gender,
            phone=instance.phone,
            email=instance.email,
            address=instance.address,
            links={"all": f"{base_url}/api/v1{router.prefix}"}
        )

@router.get(path="/{user_id}", status_code=200)
async def get_concrete_user(request: Request, session: SessionDep, user_id:int) -> UserSchemaResponse:
    base_url = str(request.base_url).rstrip('/')
    try:
        user = await UserRepository.get_user_by_id(session, user_id)
        return  UserSchemaResponse(
                first_name=user.first_name,
                last_name=user.last_name,
                gender=user.gender,
                phone=user.phone,
                email=user.email,
                address=user.address,
                links={"all": f"{base_url}/api/v1{router.prefix}"}
            )
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Пользователь с id={user_id} не найден")
    
@router.post(path="/load_from_api", status_code=202)
async def load_new_users_from_api(load: LoadNewUsers, background_task: BackgroundTasks) -> JSONResponse:
    background_task.add_task(loader_random_users, load.count)
    return JSONResponse(
        status_code=202,
        content={"message": "Loading started", "count": load.count}
    )