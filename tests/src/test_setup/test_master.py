# pylint: disable = too-many-arguments, too-many-positional-arguments
"""Module to test the setup of the master repository."""

from unittest.mock import patch
from src.setup._master import Master
from src.utils.directory import Directory

@patch("src.setup._master.Docker.Container.delete")
def test_master_docker_clear(mock_delete):
    """Test the master Docker clear method."""
    Master.Docker.clear(simulation=True)
    assert mock_delete.call_count == 5

@patch("src.setup._master.Docker.Compose.up")
@patch("src.setup._master.Docker.Compose.Combined.up")
def test_master_docker_up(mock_combined_up, mock_up):
    """Test the master Docker up method."""
    Master.Docker.up(simulation=True)
    mock_combined_up.assert_called_once()
    mock_up.assert_not_called()

@patch("src.setup._master.Docker.Compose.down")
@patch("src.setup._master.Docker.Compose.Combined.down")
def test_master_docker_down(mock_combined_down, mock_down):
    """Test the master Docker down method."""
    Master.Docker.down(simulation=False)
    mock_down.assert_called_once()
    mock_combined_down.assert_not_called()

@patch("src.setup._master.Docker.Compose.status")
@patch("src.setup._master.Docker.Compose.Combined.status")
def test_master_docker_status(mock_combined_status, mock_status):
    """Test the master Docker status method."""
    Master.Docker.status(simulation=True)
    mock_combined_status.assert_called_once()
    mock_status.assert_not_called()

@patch("src.setup._master.Docker.Compose.logs")
@patch("src.setup._master.Docker.Compose.Combined.logs")
def test_master_docker_logs(mock_combined_logs, mock_logs):
    """Test the master Docker logs method."""
    Master.Docker.logs(simulation=False)
    mock_logs.assert_called_once()
    mock_combined_logs.assert_not_called()

@patch("src.setup._master.Master.Docker.down")
@patch("src.setup._master.Master.Docker.clear")
@patch("src.setup._master.Master.Docker.build")
@patch("src.setup._master.Master.Docker.up")
@patch("src.setup._master.Master.Docker.status")
@patch("src.setup._master.Master.Docker.logs")
def test_master_docker_restart(mock_logs, mock_status, mock_up, mock_build, mock_clear, mock_down):
    """Test the master Docker restart method."""
    Master.Docker.restart(simulation=False, rebuild=True)
    mock_down.assert_called_once()
    mock_clear.assert_called_once()
    mock_build.assert_called_once()
    mock_up.assert_called_once()
    mock_status.assert_called_once()
    mock_logs.assert_called_once()

@patch("src.setup._master.Docker.Desktop.start")
@patch("src.setup._master.Environment.Files.generate")
@patch("src.setup._master.Master.Docker.restart")
def test_master_setup(mock_restart, mock_generate, mock_docker_start):
    """Test the master setup method."""
    Master.setup(simulation=True, rebuild=False, start_docker_desktop=True)
    mock_docker_start.assert_called_once()
    mock_generate.assert_called_once()
    mock_restart.assert_called_once_with(True, False)

@patch("src.setup._master.Docker.Compose.build")
@patch("src.setup._master.Docker.Compose.Combined.build")
def test_master_docker_build(mock_combined_build, mock_build):
    """Test the master Docker build method."""
    Master.Docker.build(simulation=True, rebuild=True)
    mock_combined_build.assert_called_once()
    mock_build.assert_called_once_with(Directory.Repo.frontend(), npm=True, reinstall=True)

@patch("src.setup._master.Docker.Compose.build")
def test_master_docker_build_no_rebuild(mock_build):
    """Test the master Docker build method with no rebuild."""
    Master.Docker.build(simulation=False, rebuild=False)
    mock_build.assert_called_once_with(Directory.Repo.frontend(), npm=True, reinstall=False)

@patch("src.setup._master.Docker.Compose.build")
@patch("src.setup._master.Docker.Compose.Combined.build")
def test_master_docker_build_no_simulation(mock_combined_build, mock_build):
    """Test the master Docker build method with no simulation."""
    Master.Docker.build(simulation=False, rebuild=True)
    mock_build.assert_any_call(Directory.Repo.frontend(), npm=True, reinstall=True)
    mock_build.assert_any_call(Directory.root())
    mock_combined_build.assert_not_called()

@patch("src.setup._master.Docker.Compose.up")
@patch("src.setup._master.Docker.Compose.Combined.up")
def test_master_docker_up_not_simulation(mock_combined_up, mock_up):
    """Test the master Docker up method with no simulation."""
    Master.Docker.up(simulation=False)
    mock_up.assert_called_once()
    mock_combined_up.assert_not_called()

@patch("src.setup._master.Docker.Compose.Combined.down")
@patch("src.setup._master.Docker.Compose.down")
def test_master_docker_down_simulation(mock_down, mock_combined_down):
    """Test the master Docker down method with simulation."""
    Master.Docker.down(simulation=True)
    mock_combined_down.assert_called_once()
    mock_down.assert_not_called()

@patch("src.setup._master.Docker.Compose.Combined.status")
@patch("src.setup._master.Docker.Compose.status")
def test_master_docker_status_not_simulation(mock_status, mock_combined_status):
    """Test the master Docker status method with no simulation."""
    Master.Docker.status(simulation=False)
    mock_status.assert_called_once()
    mock_combined_status.assert_not_called()

@patch("src.setup._master.Docker.Compose.Combined.logs")
@patch("src.setup._master.Docker.Compose.logs")
def test_master_docker_logs_simulation(mock_logs, mock_combined_logs):
    """Test the master Docker logs method with simulation."""
    Master.Docker.logs(simulation=True)
    mock_combined_logs.assert_called_once()
    mock_logs.assert_not_called()
