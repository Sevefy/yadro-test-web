from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_get_users_empty(client: AsyncClient):
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, user):
    response = await client.get(f"/api/v1/users/{user.id}")
    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, dict)
    assert data["first_name"] == user.first_name

@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient, user):
    response = await client.get("/api/v1/users/2")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_random_user_empty(client: AsyncClient):
    response = await client.get("/api/v1/users/random")
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_random_user(client: AsyncClient, user):
    response = await client.get("/api/v1/users/random")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "limit, offset, expected_count",
    [
        (10, 0, 10),
        (25, 25, 25),
        (10, 3000, 0),
    ]
)
async def test_get_users_with_pagination(limit, offset, expected_count,  client, users):
    response = await client.get("/api/v1/users", params={"limit": limit, "offset": offset})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == expected_count
    if len(data):
        assert data[0]["first_name"] == users[offset].first_name 
