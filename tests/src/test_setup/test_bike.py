from unittest.mock import patch
from src.setup._bike import Bike

@patch("src.setup._bike.Bike.Docker._build")
@patch("src.setup._bike.Bike._env")
def test_bike_setup(mock_env, mock_docker_build):
    Bike.setup(bikes=[{"id": 101}], docker=True)
    mock_docker_build.assert_called_once()
    mock_env.assert_called_once_with([{"id": 101}])

@patch("src.setup._bike.Bike.Docker._up")
@patch("src.setup._bike.Bike.Docker.status")
@patch("src.setup._bike.Bike.Docker.logs")
def test_bike_run_docker(mock_logs, mock_status, mock_up):
    Bike.run()
    mock_up.assert_called_once()
    mock_status.assert_called_once()
    mock_logs.assert_called_once()

@patch("src.setup._bike.Bike.Docker._build")
@patch("src.setup._bike.Bike._venv")
@patch("src.setup._bike.Bike._env")
def test_bike_setup_no_docker(mock_env, mock_venv, mock_build):
    """
    If docker=False, Bike.setup should call _venv() but not ._build().
    """
    bikes = [{"id": 111}]
    Bike.setup(bikes=bikes, docker=False)

    # _venv should be called
    mock_venv.assert_called_once()
    # _build should NOT be called
    mock_build.assert_not_called()
    # _env should be called with provided bikes
    mock_env.assert_called_once_with(bikes)
