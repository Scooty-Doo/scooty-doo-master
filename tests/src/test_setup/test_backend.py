from unittest.mock import patch
from src.setup._backend import Backend

@patch("src.setup._backend.Docker.Desktop.start")
@patch("src.setup._backend.Docker.Compose.up")
@patch("src.setup._backend.Command.run")
def test_database_setup(mock_cmd_run, mock_docker_up, mock_docker_desktop_start):
    Backend._database()
    # Should have started Docker Desktop, spun up containers, and run table_creation_module
    mock_docker_desktop_start.assert_called_once()
    mock_docker_up.assert_called_once()
    # Check final call to run table_creation_module
    assert any("api.db.table_creation" in call[0][0] for call in mock_cmd_run.call_args_list)

@patch("src.setup._backend.Command.run")
def test_mock_data_load(mock_cmd_run):
    Backend._mock_data()
    # Should call "database.load_mock_data"
    mock_cmd_run.assert_called_once()
    args = mock_cmd_run.call_args[0][0]
    # e.g. [PYTHON_EXECUTABLE, '-m', 'database.load_mock_data']
    assert "database.load_mock_data" in args

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

@patch("src.setup._backend.Command.run")
def test_start_server_no_docker(mock_cmd_run):
    """
    _start_server(docker=False)
    """
    Backend._start_server(docker=False)
    # Should NOT call Docker stuff
    mock_cmd_run.assert_called_once()
    args = mock_cmd_run.call_args[0][0]
    assert "uvicorn" in args
    assert "api.main:app" in args

@patch("src.setup._backend.Backend._venv")
@patch("src.setup._backend.Backend._database")
@patch("src.setup._backend.Backend._mock_data")
@patch("src.setup._backend.Backend.Docker._build")
def test_setup_with_docker(mock_build, mock_mock_data, mock_database, mock_venv):
    Backend.setup(docker=True)
    mock_venv.assert_called_once()
    mock_database.assert_called_once()
    mock_mock_data.assert_called_once()
    mock_build.assert_called_once()

@patch("src.setup._backend.Backend._venv")
@patch("src.setup._backend.Backend._database")
@patch("src.setup._backend.Backend._mock_data")
@patch("src.setup._backend.Backend.Docker._build")
def test_setup_no_docker(mock_build, mock_mock_data, mock_database, mock_venv):
    """
    If docker=False, we skip the Docker._build step.
    """
    Backend.setup(docker=False)
    mock_venv.assert_called_once()
    mock_database.assert_called_once()
    mock_mock_data.assert_called_once()
    mock_build.assert_not_called()
