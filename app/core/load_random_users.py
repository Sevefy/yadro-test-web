import json
from typing import Any

import aiohttp

from app.database import AsyncSessionLocal, get_session
from app.models.users import UserModel
from app.repository.users import UserRepository
from app.config import logger


async def get_users_from_randomdatatools(count: int):
    if count < 1:
        return
    
    url = "https://api.randomdatatools.ru/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={"count": count}) as resp:
            if resp.status != 200:
                logger.error(f"API error: {resp.status}")
                resp.raise_for_status()
            content = await resp.text()
            data = json.loads(content)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            else:
                logger.error("API returned unexpected data format")
                raise ValueError
    
async def loader_random_users(count=1000):
    if count < 1:
        return
    logger.info("Started loader user info from randomdatatools")

    MAX_PER_REQUEST = 100
    batch_size = min(count, MAX_PER_REQUEST)
    
    loaded = 0
    while loaded < count:
        need = min(batch_size, count - loaded)
        try:
            data = await get_users_from_randomdatatools(need)
            await load_data_db(data)
            loaded += len(data)
            logger.info(f"Loaded {loaded}/{count} users")
        except Exception as e:
            logger.error(f"API request error {e}")
            break
    logger.info("Completed loader user info from randomdatatools")

    
async def load_data_db(users: list[dict[str: Any]]):
    models = [
        UserModel(
            first_name=user.get("FirstName"),
            last_name=user.get("LastName"),
            gender=user.get("Gender"),
            phone=user.get("Phone"),
            email=user.get("Email"),
            address=user.get("Address"),
        )
        for user in users
    ]
    async with AsyncSessionLocal() as session:
        await UserRepository.create_users_dump(session, users)


