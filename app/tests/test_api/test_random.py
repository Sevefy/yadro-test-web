import httpx
import pytest
from unittest import mock
import respx

from app.core.load_random_users import get_users_from_randomdatatools, loader_random_users

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "api_return, count_need, expected_calls",  
    [
        ([1], 1, 1), 
        ([{}], 1, 1),
    ]
)
async def test_get_random_users(api_return, count_need, expected_calls):
    with mock.patch("app.core.load_random_users.get_users_from_randomdatatools") as mock_api, \
         mock.patch("app.core.load_random_users.load_data_db") as mock_load:
        mock_api.return_value = api_return
        await loader_random_users(count_need)
        assert mock_api.call_count == expected_calls
        mock_load.assert_called()
            
@pytest.mark.asyncio
async def test_loader_random_users_api_error():
    with mock.patch("app.core.load_random_users.get_users_from_randomdatatools") as mock_api, \
         mock.patch("app.core.load_random_users.load_data_db") as mock_load:
        mock_api.side_effect = httpx.HTTPError("Error")
        await loader_random_users(10)
        mock_api.assert_called()
        mock_load.assert_not_called()
        
@pytest.mark.asyncio
async def test_loader_random_users_api_value_error():
    with mock.patch("app.core.load_random_users.get_users_from_randomdatatools") as mock_api, \
         mock.patch("app.core.load_random_users.load_data_db") as mock_load:
        mock_api.side_effect = ValueError
        await loader_random_users(10)
        mock_api.assert_called()
        mock_load.assert_not_called()


# Добавить в requirements.txt: respx
@pytest.mark.asyncio
@respx.mock
async def test_get_random_users_with_respx():
    respx.get("https://api.randomdatatools.ru/").mock(
        return_value=httpx.Response(
            200, 
            json={
                "FirstName": "Иван",
                "LastName": "Иванов",
                "Gender": "Мужчина",
                "Phone": "+7 (999) 999-99-99",
                "Email": "ivan@test.ru",
                "Address": "Москва"
            }
        )
    )
    
    result = await get_users_from_randomdatatools(1)
    
    assert len(result) == 1
    assert result[0]["FirstName"] == "Иван"
    
    
@pytest.mark.asyncio
@respx.mock
async def test_get_random_users_error_with_respx():
    respx.get("https://api.randomdatatools.ru/").mock(
        return_value=httpx.Response(500)
    )
    
    with pytest.raises(httpx.HTTPStatusError):
        await get_users_from_randomdatatools(1)
