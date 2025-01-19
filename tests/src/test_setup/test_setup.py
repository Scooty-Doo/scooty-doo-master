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

def test_setup_backend():
    with patch("src.setup.setup.Backend.run") as mock_backend_run:
        Setup.backend()
        mock_backend_run.assert_called_once()

def test_setup_bike_no_bikes():
    with patch("builtins.print") as mock_print, \
         patch("src.setup.setup.Bike.setup") as mock_bike_setup, \
         patch("src.setup.setup.Bike.run") as mock_bike_run:
        Setup.bike(start_server=True, bikes=None, already_setup=False, docker=True)
        mock_print.assert_called_once_with("No bikes provided to generate .env file for.")
        mock_bike_setup.assert_called_once_with(None, docker=True)
        mock_bike_run.assert_called_once()

def test_setup_master():
    with patch("src.setup.setup.Master.setup") as mock_master_setup:
        Setup.master(simulation=True, rebuild=False)
        mock_master_setup.assert_called_once_with(True, False)
    with patch("src.setup.setup.Master.setup") as mock_master_setup:
        Setup.master(simulation=False, rebuild=True)
        mock_master_setup.assert_called_once_with(False, True)
