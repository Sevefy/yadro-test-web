from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app.db"

# создаем асинхронный движок (Async Engine)
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# базовый класс для моделей 
class Base(DeclarativeBase):
    pass

# асинхронный генератор
async def get_session():
    # Используем async with — это гарантирует, что сессия закроется корректно
    async with AsyncSessionLocal() as session:
        yield session

async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
        await conn.run_sync(Base.metadata.create_all) 
        
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]