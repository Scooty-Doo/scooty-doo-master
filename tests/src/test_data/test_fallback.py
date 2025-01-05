import pytest
from unittest.mock import patch
from src.data._fallback import Fallback

@patch("src.data._fallback.File.Load.from_csv")
@patch("src.data._fallback.File.Convert.csv_to_json")
def test_fallback_bikes(mock_csv_to_json, mock_from_csv):
    mock_from_csv.return_value = "id,name\n101,Bike1"
    mock_csv_to_json.return_value = [{"id": "101", "name": "Bike1"}]
    result = Fallback.bikes(save_to_json=False)
    mock_from_csv.assert_called_once()
    mock_csv_to_json.assert_called_once_with("id,name\n101,Bike1")
    assert result == [{"id": "101", "name": "Bike1"}]

@patch("src.data._fallback.File.Save.to_json")
def test_fallback_bikes_save(mock_save_to_json):
    with patch("src.data._fallback.File.Load.from_csv", return_value="fake csv"):
        with patch("src.data._fallback.File.Convert.csv_to_json", return_value=[{"id": "fake"}]):
            Fallback.bikes(save_to_json=True)
            mock_save_to_json.assert_called_once()

@patch("src.data._fallback.File.Load.from_csv", return_value="id,name\n201,Jesus")
@patch("src.data._fallback.File.Convert.csv_to_json", return_value=[{"id": "201", "name": "Jesus"}])
def test_fallback_trips(mock_csv_to_json, mock_from_csv):
    with patch("src.data._fallback.File.Save.to_json") as mock_save:
        result = Fallback.trips(save_to_json=False)
        mock_save.assert_not_called()
        assert result == [{"id": "201", "name": "Jesus"}]

@patch("src.data._fallback.File.Load.from_csv")
def test_fallback_trips_file_not_found(mock_from_csv):
    mock_from_csv.side_effect = FileNotFoundError("CSV missing")
    with pytest.raises(FileNotFoundError):
        Fallback.trips()

@patch("src.data._fallback.File.Load.from_csv", return_value="id,name\n301,User1")
@patch("src.data._fallback.File.Convert.csv_to_json", return_value=[{"id": "301", "name": "User1"}])
def test_fallback_users(mock_csv_to_json, mock_from_csv):
    with patch("src.data._fallback.File.Save.to_json") as mock_save:
        result = Fallback.users(save_to_json=False)
        mock_save.assert_not_called()
        assert result == [{"id": "301", "name": "User1"}]

@patch("src.data._fallback.File.Load.from_csv")
@patch("src.data._fallback.File.Convert.csv_to_json")
@patch("src.data._fallback.File.Save.to_json")
def test_fallback_zones(mock_save_to_json, mock_csv_to_json, mock_from_csv):
    mock_from_csv.return_value = "id,name\n1,TestZone"
    mock_csv_to_json.return_value = [{"id": "1", "name": "TestZone"}]
    result = Fallback.zones(save_to_json=True)
    mock_from_csv.assert_called_once()
    mock_csv_to_json.assert_called_once_with("id,name\n1,TestZone")
    mock_save_to_json.assert_called_once()
    assert result == [{"id": "1", "name": "TestZone"}]

@patch("src.data._fallback.File.Load.from_csv", return_value="id,name\n1,TypeA")
@patch("src.data._fallback.File.Convert.csv_to_json", return_value=[{"id": "1", "name": "TypeA"}])
@patch("src.data._fallback.File.Save.to_json")
def test_fallback_zone_types(mock_save_to_json, mock_csv_to_json, mock_from_csv):
    result = Fallback.zone_types(save_to_json=False)
    mock_from_csv.assert_called_once()
    mock_csv_to_json.assert_called_once()
    mock_save_to_json.assert_not_called()
    assert result == [{"id": "1", "name": "TypeA"}]
