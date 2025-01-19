from unittest.mock import patch
import pytest
from src.setup._frontend import Frontend

@patch("src.setup._frontend.Frontend.Docker._start")
@patch("src.setup._frontend.Frontend.Docker.status")
@patch("src.setup._frontend.Frontend.Docker.logs")
def test_frontend_run(mock_logs, mock_status, mock_start):
    Frontend.run()
    mock_start.assert_called_once()
    mock_status.assert_called_once()
    mock_logs.assert_called_once()

@patch("src.setup._frontend.Environment.Files.generate")
@patch("src.setup._frontend.Frontend.Docker._build")
def test_frontend_setup(mock_build, mock_generate):
    Frontend.setup()
    mock_generate.assert_called_once_with(frontend=True)
    mock_build.assert_called_once()

@patch("src.setup._frontend.Frontend.Docker._build")
@patch("src.setup._frontend.Frontend.Docker._start")
@patch("src.setup._frontend.Frontend.Docker.status")
@patch("src.setup._frontend.Frontend.Docker.logs")
def test_frontend_full(mock_logs, mock_status, mock_start, mock_build):
    frontend = Frontend()
    frontend.setup()
    frontend.run()
    frontend.Docker.status()

    mock_build.assert_called_once()
    mock_start.assert_called_once()
    mock_status.assert_called()
    mock_logs.assert_called()

@patch("src.setup._frontend.Docker.Compose.build")
@patch("src.setup._frontend.Docker.Compose.up")
@patch("src.setup._frontend.Docker.Compose.status")
@patch("src.setup._frontend.Docker.Compose.logs")
def test_frontend_docker(mock_logs, mock_status, mock_up, mock_build):
    Frontend.Docker._build()
    mock_build.assert_called_once()
    Frontend.Docker._start()
    mock_up.assert_called_once()
    Frontend.Docker.status()
    mock_status.assert_called_once()
    Frontend.Docker.logs()
    mock_logs.assert_called_once()

@patch("src.setup._frontend.Docker.Compose.up", side_effect=Exception("Docker up failed"))
def test_frontend_docker_start_failure(mock_up):
    with pytest.raises(SystemExit):
        Frontend.Docker._start()
    mock_up.assert_called_once()

@patch("src.setup._frontend.Docker.Compose.build", side_effect=Exception("Docker build failed"))
def test_frontend_docker_build_failure(mock_build):
    with pytest.raises(SystemExit):
        Frontend.Docker._build()
    mock_build.assert_called_once()
