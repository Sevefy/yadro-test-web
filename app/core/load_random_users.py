import asyncio
import json
from typing import Any

import httpx
from app.database import AsyncSessionLocal
from app.models.users import UserModel
from app.repository.users import UserRepository
from app.config import logger
from functools import wraps
from sqlalchemy.exc import IntegrityError

def retry(func=None, max_retries: int = 3, delay_multiplier: int = 2):
    def decorator(func):        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    result = await func(*args, **kwargs)
                    return result
                except (httpx.HTTPStatusError, httpx.RequestError, json.JSONDecodeError) as e:
                    logger.warning(f"Attempt {attempt}/{max_retries} failed {e}, retry...")
                    delay = delay_multiplier * (2 ** (attempt - 1))     
                    await asyncio.sleep(delay)
                    last_exception = e
            raise last_exception
        return wrapper
    if func is None:
        return decorator
    return decorator(func)    

@retry(max_retries=5)
async def get_users_from_randomdatatools(count: int):
    if count < 1:
        return
    
    url = "https://api.randomdatatools.ru/"
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.get(url, params={"count": count})
        if resp.status_code != 200:
            logger.error(f"API error: {resp.status_code}")
            resp.raise_for_status()
            
        data = resp.json()
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
        except IntegrityError as e:
            logger.error(f"Error load data DB {e}")
        except Exception as e:
            logger.error(f"API request error {e}")
            break
    logger.info("Completed loader user info from randomdatatools")

    
async def load_data_db(users: list[dict[str, Any]]):
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
    try:
        async with AsyncSessionLocal() as session:
            await UserRepository.create_users_dump(session, models)
    except IntegrityError:
        raise

