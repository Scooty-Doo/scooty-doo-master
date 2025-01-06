from unittest.mock import patch
from src.setup._backend import Backend

@patch("src.setup._backend.Docker.Desktop.start")
@patch("src.setup._backend.Docker.Compose.up")
@patch("src.setup._backend.Command.run")
def test_database_setup_success(mock_cmd_run, mock_docker_up, mock_desktop_start):
    """
    Check the happy path where Docker Desktop starts,
    Docker containers come up, and table creation runs.
    """
    Backend._database()
    mock_desktop_start.assert_called_once()
    mock_docker_up.assert_called_once()
    # Check we eventually run the "api.db.table_creation" command
    assert any("api.db.table_creation" in call[0][0] for call in mock_cmd_run.call_args_list)

@patch("src.setup._backend.Backend.Docker._up")
@patch("src.setup._backend.Backend.Docker.status")
@patch("src.setup._backend.Backend.Docker.logs")
def test_start_server_docker(mock_logs, mock_status, mock_up):
    """
    _start_server(docker=True)
    """
    Backend._start_server(docker=True)
    mock_up.assert_called_once()
    mock_status.assert_called_once()
    mock_logs.assert_called_once()
