import pytest
import requests
from unittest.mock import patch, MagicMock
from src.data.get import Get

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("BACKEND_URL", "http://localhost:8000/")
    monkeypatch.setenv("TOKEN", "test_token")

@patch("src.data.get.requests.get")
def test_get_bikes_success(mock_get):
    """
    Should return data from the backend if requests.get succeeds.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"id": "1"}, {"id": "2"}]}
    mock_response.raise_for_status.return_value = None  # no error
    mock_get.return_value = mock_response

    get = Get()
    result = get.bikes(save_to_json=False)
    assert result == [{"id": "1"}, {"id": "2"}]
    mock_get.assert_called_once()

@patch("src.data.get.requests.get", side_effect=Exception("Connection error"))
def test_get_bikes_fallback(mock_get):
    get = Get()
    with pytest.raises(Exception):
        get.bikes()
 
@pytest.mark.parametrize("method_name", ["bikes", "trips", "users", "zones", "zone_types"])
@patch("src.data.get.requests.get")
def test_get_no_save_to_json(mock_get, method_name):
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"id": "123"}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    get = Get()
    method_to_call = getattr(get, method_name)
    with patch("src.data.get.File.Save.to_json") as mock_save:
        result = method_to_call(save_to_json=False)
        mock_save.assert_not_called()
        assert result == [{"id": "123"}]

@pytest.mark.parametrize("method_name", ["bikes", "trips", "users", "zones", "zone_types"])
@patch("src.data.get.requests.get")
def test_get_save_to_json(mock_get, method_name):
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": [{"id": "999"}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    get = Get()
    method_to_call = getattr(get, method_name)
    with patch("src.data.get.File.Save.to_json") as mock_save:
        result = method_to_call(save_to_json=True)
        mock_save.assert_called_once()
        assert result == [{"id": "999"}]

@patch("src.data.get.requests.get", side_effect=requests.exceptions.Timeout("Timeout error"))
def test_get_bikes_timeout(mock_get):
    get = Get()
    with pytest.raises(requests.exceptions.RequestException) as exc:
        get.bikes()
    assert "Timeout error" in str(exc.value)
