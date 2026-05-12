import json
from typing import Any

import aiohttp

from app.database import AsyncSessionLocal
from app.models.users import UserModel


async def loader_random_users():
    url = "https://api.randomdatatools.ru/"
    count = 100
    for i in range(10):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"count": count}) as resp:
                content = await resp.text()
                await load_data_db(json.loads(content))
    
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
        try:
            db_session.add_all(models)
            await db_session.commit()
        except Exception as e:
            print(f"Error saving to database: {e}")
            await db_session.rollback()

