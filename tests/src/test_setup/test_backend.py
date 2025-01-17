# pylint: disable=protected-access, too-many-arguments, too-many-positional-arguments
"""Module to test the setup of the backend server."""

from unittest.mock import patch
import pytest
from src.setup._backend import Backend

@patch("src.setup._backend.Docker.Compose.build")
@patch("src.setup._backend.Docker.Compose.up")
@patch("src.setup._backend.Docker.Compose.down")
@patch("src.setup._backend.Docker.Compose.status")
@patch("src.setup._backend.Docker.Compose.logs")
@patch("src.setup._backend.Docker.Container.delete")
def test_backend_docker(mock_delete, mock_logs, mock_status, mock_down, mock_up, mock_build):
    """Test the backend Docker setup."""
    Backend.Docker._build()
    mock_build.assert_called_once()
    Backend.Docker._up()
    mock_up.assert_called_once()
    Backend.Docker._down()
    mock_down.assert_called_once()
    Backend.Docker.status()
    mock_status.assert_called_once()
    Backend.Docker.logs()
    mock_logs.assert_called_once()
    Backend.Docker._clear()
    assert mock_delete.call_count == 3

@patch("src.setup._backend.Docker.Compose.down", side_effect=Exception("Docker down failed"))
def test_backend_docker_down_failure(mock_down):
    """Test backend Docker down failure."""
    with pytest.raises(SystemExit):
        Backend.Docker._down()
    mock_down.assert_called_once()

@patch("src.setup._backend.Docker.Compose.up", side_effect=Exception("Docker up failed"))
def test_backend_docker_up_failure(mock_up):
    """Test backend Docker up failure."""
    with pytest.raises(SystemExit):
        Backend.Docker._up()
    mock_up.assert_called_once()

@patch("src.setup._backend.Docker.Compose.build", side_effect=Exception("Docker build failed"))
def test_backend_docker_build_failure(mock_build):
    """Test backend Docker build failure."""
    with pytest.raises(SystemExit):
        Backend.Docker._build()
    mock_build.assert_called_once()

@patch("src.setup._backend.Backend.Docker._down")
@patch("src.setup._backend.Backend.Docker._up")
def test_backend_docker_restart(mock_up, mock_down):
    """Test backend Docker restart."""
    Backend.Docker._restart()
    mock_down.assert_called_once()
    mock_up.assert_called_once()

@patch("src.setup._backend.Backend.Docker._down")
@patch("src.setup._backend.Backend.Docker._clear")
@patch("src.setup._backend.Backend.Docker._build")
@patch("src.setup._backend.Backend.Docker._up")
@patch("src.setup._backend.Backend.Docker.status")
@patch("src.setup._backend.Backend.Docker.logs")
def test_backend_setup(mock_logs, mock_status, mock_up, mock_build, mock_clear, mock_down):
    """Test the backend setup."""
    Backend._setup()
    mock_down.assert_called_once() # pylint: disable=duplicate-code
    mock_clear.assert_called_once() # pylint: disable=duplicate-code
    mock_build.assert_called_once() # pylint: disable=duplicate-code
    mock_up.assert_called_once() # pylint: disable=duplicate-code
    mock_status.assert_called_once() # pylint: disable=duplicate-code
    mock_logs.assert_called_once() # pylint: disable=duplicate-code

@patch("src.setup._backend.Backend._setup")
def test_backend_run(mock_setup):
    """Test running the backend."""
    Backend.run()
    mock_setup.assert_called_once()
