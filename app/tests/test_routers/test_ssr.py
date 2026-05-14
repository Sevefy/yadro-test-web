import pytest

@pytest.mark.asyncio
async def test_index_page_pagination(client, users):
    # Первая страница
    response = await client.get("/?limit=25&offset=0")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 200
    assert "Страница 1 из" in response.text
    
    # Вторая страница
    response = await client.get("/?limit=25&offset=25")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 200
    assert "Страница 2 из" in response.text
    assert users[25].first_name in response.text


@pytest.mark.asyncio
async def test_index_empty(client):
    response = await client.get("")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 200
    assert "всего 0" in response.text.lower()

@pytest.mark.asyncio
async def test_index_1000(client, users):
    response = await client.get("")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 200
    assert "всего 1000" in response.text.lower()

@pytest.mark.asyncio
async def test_concrete_user(client, user):
    response = await client.get(f"/{user.id}")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 200
    assert user.first_name in response.text
    
    
@pytest.mark.asyncio
async def test_concrete_user_not_found(client, user):
    response = await client.get("/999999")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 404
    assert "Пользователь с id=999999 не найден" in response.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id", [
        "t",
        1.1
    ]
)
async def test_concrete_user_incorrect_id(client, user, user_id):
    response = await client.get(f"/{user_id}")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_random_user(client, user):
    response = await client.get("/random")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_random_user_empty(client):
    response = await client.get("/random")
    assert "text/html" in response.headers["content-type"]
    assert response.status_code == 404
    assert "Нет пользователей" in response.text
    