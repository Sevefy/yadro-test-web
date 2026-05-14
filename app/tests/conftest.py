
import pytest
from faker import Faker
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_session
from app.main import app
from app.models.users import UserModel

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

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


async def override_get_session():
    # Используем async with — это гарантирует, что сессия закроется корректно
    async with AsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(autouse=True)
async def setup_db():
    # Создаем все таблицы перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield         
    async with engine.begin() as conn:        
        await conn.run_sync(Base.metadata.drop_all) 

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
        
@pytest.fixture
async def user():
    instance = UserModel(
        first_name="Федор",
        last_name="Ященко",
        gender="Мужчина",
        phone="+7 (959) 202-61-47",
        email="fedor.semichaevskiy@mail.ru",
        address="Россия, г. Тольятти, Почтовая ул., д. 17 кв.174"
    )
    async with AsyncSessionLocal() as session:
        session.add(instance)
        await session.commit()
    return instance


@pytest.fixture
async def users():
    fake = Faker("ru_RU")
    instances = []
    for i in range(1000):
        user = UserModel(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            gender=fake.random_element(elements=("Мужчина", "Женщина")),
            phone=fake.phone_number(),
            email=f"user{i}@test.ru",
            address=fake.address(),
        )
        instances.append(user)
    async with AsyncSessionLocal() as session:
        session.add_all(instances)
        await session.commit()
        return instances