"""Tests for the Get class"""

from unittest.mock import AsyncMock, Mock, patch
import pytest
import httpx
from src.data.get import Get

@pytest.mark.asyncio
class TestGet:
    """Tests for the Get class"""
    @pytest.fixture
    def _mock_settings(self):
        """Mock the Settings class."""
        with patch('src.data.get.Settings') as mock_settings:
            mock_endpoints = Mock()
            mock_endpoints.backend_url = 'https://api.example.com'
            mock_endpoints.Bikes.get_all = 'bikes'
            mock_endpoints.Trips.get_all = 'trips'
            mock_endpoints.Users.get_all = 'users'
            mock_endpoints.Zones.get_all = 'zones'
            mock_endpoints.Zones.get_types = 'zone_types'
            mock_settings.Endpoints.return_value = mock_endpoints
            mock_settings.Endpoints.token = 'test_token'
            mock_settings.Directory.data = '/test/data'
            yield mock_settings

    @pytest.fixture
    def _mock_file(self):
        """Mock the File.Save class."""
        with patch('src.data.get.File.Save.to_json', new_callable=AsyncMock) as mock_save:
            yield mock_save

    @pytest.fixture
    def mock_httpx(self):
        """Mock the httpx.AsyncClient class."""
        with patch('src.data.get.httpx.AsyncClient') as mock_client:
            mock_instance = mock_client.return_value.__aenter__.return_value
            mock_instance.get = AsyncMock()
            mock_instance.get.return_value.json = Mock(
                return_value={'data': [{'id': 1, 'name': 'test'}]})
            mock_instance.get.return_value.raise_for_status = Mock()
            yield mock_instance

    @pytest.mark.parametrize("method,filename,endpoint", [
        ('bikes', 'bikes.json', 'bikes'),
        ('trips', 'trips.json', 'trips'),
        ('users', 'users.json', 'users'),
        ('zones', 'zones.json', 'zones'),
        ('zone_types', 'zone_types.json', 'zone_types')
    ])

    async def test_get_methods(
        self, _mock_settings, _mock_file, mock_httpx, method,
        filename, endpoint):
        """Test the get methods."""
        get_instance = Get()
        get_method = getattr(get_instance, method)
        result = await get_method()
        expected_params = {"limit": 9999}
        if method == 'users':
            expected_params["is_eligable"] = True
        mock_httpx.get.assert_awaited_once_with(
            f'https://api.example.com/{endpoint}',
            params=expected_params,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer test_token',
            },
            timeout=20.0
        )
        _mock_file.assert_awaited_once_with(
            data=[{'id': 1, 'name': 'test'}],
            folder='/test/data', filename=filename)
        assert result == [{'id': 1, 'name': 'test'}]

    async def test_get_request_error(self, _mock_settings, _mock_file, mock_httpx):
        """Test the get method with a request error."""
        mock_httpx.get.side_effect = httpx.RequestError("Request failed")
        get_instance = Get()
        with pytest.raises(httpx.RequestError):
            await get_instance.bikes()

    async def test_users_request_error(self, _mock_settings, _mock_file, mock_httpx):
        """Test the users method with a request error."""
        mock_httpx.get.side_effect = httpx.RequestError("Request failed")
        get_instance = Get()
        with pytest.raises(httpx.RequestError) as exc_info:
            await get_instance.users()
        assert "Failed to request" in str(exc_info.value)
