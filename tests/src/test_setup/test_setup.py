from unittest.mock import patch
from src.setup.setup import Setup

@patch("src.setup.setup.Bike.setup")
@patch("src.setup.setup.Bike.run")
def test_setup_bike(mock_bike_run, mock_bike_setup):
    Setup.bike(
        start_server=True, bikes=[{"id": 101}],
        already_setup=False,
        docker=True)
    mock_bike_setup.assert_called_once_with(
        [{"id": 101}], docker=True)
    mock_bike_run.assert_called_once()

@patch("src.setup.setup.Frontend.setup")
@patch("src.setup.setup.Frontend.run")
def test_setup_frontend(mock_frontend_run, mock_frontend_setup):
    Setup.frontend(start_server=True, already_setup=False)
    mock_frontend_setup.assert_called_once()
    mock_frontend_run.assert_called_once()
