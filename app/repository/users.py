from aiosqlite import IntegrityError
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.users import UserModel
import aiosqlite
from app.config import logger

from sqlalchemy.sql.expression import func

class UserRepository:
    
    @staticmethod
    async def get_all_users(session: AsyncSession, limit: int = 50, offset: int = 0) -> list[UserModel]:
        try:    
            query = select(UserModel).limit(limit).offset(offset)
            result = await session.execute(query)
            return result.scalars().all()
        except aiosqlite.Error as e:
            logger.error(f"A database error occurred: {e}")
            raise
        
    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> UserModel:
        try:
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            user = result.scalar()
            if user is None:
                raise ValueError
            return user
        except ValueError:
            logger.error(f"Not found error: {user_id}")
            raise ValueError("Not found error")

        except SQLAlchemyError as e:
            logger.error(f"DB error getting users count: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_random_user(session: AsyncSession) -> UserModel:
        try:
            query = select(UserModel).order_by(func.random()).limit(1)
            result = await session.execute(query)
            user = result.scalar()
            if user is None:
                raise ValueError
            return user
        except IntegrityError as e:
            logger.error(f"Integrity error getting users count: {e}")
            await session.rollback()
            raise
        except SQLAlchemyError as e:
            logger.error(f"DB error getting users count: {e}")
            await session.rollback()
            raise
        
    @staticmethod
    async def create_user(session: AsyncSession, user: UserModel) -> None:
        try:
            session.add(user)
            await session.commit()
        except IntegrityError as e:
            logger.error(f"Integrity error getting users count: {e}")
            await session.rollback()
            raise
        except SQLAlchemyError as e:
            logger.error(f"DB error getting users count: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def create_users_dump(session: AsyncSession, users: list[UserModel]) -> None:
        try:
            session.add_all(users)
            await session.commit()
        except IntegrityError as e:
            logger.error(f"Integrity error getting users count: {e}")
            await session.rollback()
            raise
        except SQLAlchemyError as e:
            logger.error(f"DB error getting users count: {e}")
            await session.rollback()
            raise
    
    @staticmethod
    async def get_total_users(session: AsyncSession) -> int:
        try:
            # Оборачиваем SQL в text()
            result = await session.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar() 
            return count if count is not None else 0
        except IntegrityError as e:
            logger.error(f"Integrity error getting users count: {e}")
            await session.rollback()
            raise
        except SQLAlchemyError as e:
            logger.error(f"DB error getting users count: {e}")
            await session.rollback()
            raise
    