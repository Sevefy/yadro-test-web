from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import UserModel


class UserRepository:
    
    @staticmethod
    async def get_all_users(session: AsyncSession, limit: int = 50, offset: int = 0) -> List[UserModel]:
        query = select(UserModel).limit(limit).offset(offset)
        result = await session.execute(query)
        return result.scalars().all()
    
        
    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> UserModel:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(query)
        return result.scalar()