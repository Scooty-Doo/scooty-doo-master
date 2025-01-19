# pylint: disable=protected-access

from unittest.mock import patch
import pytest
from src.setup._bike import Bike

@patch("src.setup._bike.Bike.Docker._up")
@patch("src.setup._bike.Bike.Docker.status")
@patch("src.setup._bike.Bike.Docker.logs")
def test_bike_run(mock_logs, mock_status, mock_up):
    Bike.run()
    mock_up.assert_called_once()
    mock_status.assert_called_once()
    mock_logs.assert_called_once()

@patch("src.setup._bike.Bike.Docker._build")
@patch("src.setup._bike.Bike._env")
@patch("src.setup._bike.Bike._venv")
def test_bike_setup(mock_venv, mock_env, mock_build):
    Bike.setup(bikes=["bike1", "bike2"], docker=True)
    mock_build.assert_called_once()
    mock_env.assert_called_once_with(["bike1", "bike2"])
    mock_venv.assert_not_called()

@patch("src.setup._bike.Bike.Docker._build")
@patch("src.setup._bike.Bike.Docker._up")
@patch("src.setup._bike.Bike.Docker.status")
@patch("src.setup._bike.Bike.Docker.logs")
def test_bike_full(mock_logs, mock_status, mock_up, mock_build):
    Bike.setup(bikes=[], docker=True)
    Bike.run()
    mock_build.assert_called_once()
    mock_up.assert_called_once()
    mock_status.assert_called()
    mock_logs.assert_called()

@patch("src.setup._bike.Docker.Compose.build")
@patch("src.setup._bike.Docker.Compose.up")
@patch("src.setup._bike.Docker.Compose.down")
@patch("src.setup._bike.Docker.Compose.status")
@patch("src.setup._bike.Docker.Compose.logs")
def test_bike_docker_compose_commands(mock_logs, mock_status, mock_down, mock_up, mock_build):
    Bike.Docker._build()
    mock_build.assert_called_once()
    Bike.Docker._up()
    mock_up.assert_called_once()
    Bike.Docker._down()
    mock_down.assert_called_once()
    Bike.Docker.status()
    mock_status.assert_called_once()
    Bike.Docker.logs()
    mock_logs.assert_called_once()

@patch("src.setup._bike.Docker.Compose.build")
@patch("src.setup._bike.Docker.Compose.up")
@patch("src.setup._bike.Docker.Compose.down", side_effect=Exception("Docker down failed"))
@patch("src.setup._bike.Docker.Compose.status")
@patch("src.setup._bike.Docker.Compose.logs")
def test_bike_docker_down_failure(_mock_logs, _mock_status, mock_down, _mock_up, _mock_build):
    with pytest.raises(SystemExit):
        Bike.Docker._down()
    mock_down.assert_called_once()

@patch("src.setup._bike.Docker.Compose.up", side_effect=Exception("Docker up failed"))
def test_bike_docker_up_failure(mock_up):
    with pytest.raises(SystemExit):
        Bike.Docker._up()
    mock_up.assert_called_once()

@patch("src.setup._bike.Docker.Compose.build", side_effect=Exception("Docker build failed"))
def test_bike_docker_build_failure(mock_build):
    with pytest.raises(SystemExit):
        Bike.Docker._build()
    mock_build.assert_called_once()

@patch("src.setup._bike.Bike.Docker._down")
@patch("src.setup._bike.Bike.Docker._up")
def test_bike_docker_restart(mock_up, mock_down):
    Bike.Docker._restart()
    mock_down.assert_called_once()
    mock_up.assert_called_once()

@patch("src.setup._bike.Venv.setup")
def test_bike_venv(mock_venv):
    Bike._venv()
    mock_venv.assert_called_once()

@patch("src.setup._bike.Command.run")
def test_bike_start_server_success(mock_run):
    Bike._start_server(docker=False)
    mock_run.assert_called_once()

@patch("src.setup._bike.Command.run", side_effect=Exception("Server start failed"))
def test_bike_start_server_command_failure(mock_run):
    with pytest.raises(SystemExit):
        Bike._start_server(docker=False)
    mock_run.assert_called_once()

@patch("src.setup._bike.Bike.Docker._build")
@patch("src.setup._bike.Bike._venv")
@patch("src.setup._bike.Bike._env")
def test_bike_setup_no_docker(mock_env, mock_venv, mock_build):
    Bike.setup(bikes=["bike1"], docker=False)
    mock_venv.assert_called_once()
    mock_build.assert_not_called()
    mock_env.assert_called_once_with(["bike1"])

@patch("src.setup._bike.Bike.Docker.status")
def test_bike_docker_status(mock_status):
    Bike.Docker.status()
    mock_status.assert_called_once()

@patch("src.setup._bike.Bike.Docker.logs")
def test_bike_docker_logs(mock_logs):
    Bike.Docker.logs()
    mock_logs.assert_called_once()

@patch("builtins.print")
def test_bike_start_server_print_success(mock_print):
    with patch("src.setup._bike.Command.run"):
        Bike._start_server(docker=False)
    mock_print.assert_any_call("FastAPI server for the bike hivemind started successfully.")
