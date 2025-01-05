from unittest.mock import patch
from src.setup._frontend import Frontend

@patch("src.setup._frontend.Frontend.Docker._build")
def test_frontend_setup(mock_build):
    Frontend.setup()
    mock_build.assert_called_once()

@patch("src.setup._frontend.Frontend.Docker._start")
@patch("src.setup._frontend.Frontend.Docker.status")
@patch("src.setup._frontend.Frontend.Docker.logs")
def test_frontend_run(mock_logs, mock_status, mock_start):
    Frontend.run()
    mock_start.assert_called_once()
    mock_status.assert_called_once()
    mock_logs.assert_called_once()
