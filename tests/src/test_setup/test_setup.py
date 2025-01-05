from unittest.mock import patch
from src.setup.setup import Setup

@patch("src.setup.setup.Backend.setup")
@patch("src.setup.setup.Backend.run")
def test_setup_backend(mock_run, mock_setup):
    Setup.backend(start_server=True, already_setup=True, docker=True)
    mock_setup.assert_not_called()
    mock_run.assert_called_once_with(True)
    Setup.backend(start_server=True, already_setup=False, docker=False)
    assert mock_setup.call_count == 1
    assert mock_run.call_count == 2

@patch("src.setup.setup.Bike.setup")
@patch("src.setup.setup.Bike.run")
def test_setup_bike(mock_bike_run, mock_bike_setup):
    Setup.bike(start_server=True, bikes=[{"id": 101}], already_setup=False, docker=True)
    mock_bike_setup.assert_called_once_with([{"id": 101}], docker=True, master_docker_compose_file=True)
    mock_bike_run.assert_called_once()

@patch("src.setup.setup.Frontend.setup")
@patch("src.setup.setup.Frontend.run")
def test_setup_frontend(mock_frontend_run, mock_frontend_setup):
    Setup.frontend(start_server=True, already_setup=False)
    mock_frontend_setup.assert_called_once()
    mock_frontend_run.assert_called_once()
