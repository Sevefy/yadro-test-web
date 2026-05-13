import aiohttp
import pytest
from unittest import mock

from app.core.load_random_users import loader_random_users

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
        mock_api.side_effect = aiohttp.ClientError("Network error")
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