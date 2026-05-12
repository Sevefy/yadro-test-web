import json
from typing import Any

import aiohttp

from app.database import AsyncSessionLocal
from app.models.users import UserModel
from app.repository.users import UserRepository
from app.config import logger

async def loader_random_users():
    url = "https://api.randomdatatools.ru/"
    count = 100
    logger.info("Started loader user info from randomdatatools")
    for i in range(10):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"count": count}) as resp:
                content = await resp.text()
                await load_data_db(json.loads(content))
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
    async with AsyncSessionLocal() as db_session:
        await UserRepository.create_users_dump(db_session, models)


