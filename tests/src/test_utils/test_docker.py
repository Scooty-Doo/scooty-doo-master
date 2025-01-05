from unittest.mock import patch
from src.utils.docker import Docker

@patch("src.utils.command.Command.run")
def test_docker_desktop_is_running_true(mock_run):
    """
    If "docker info" runs successfully, Docker.Desktop.is_running() should return True.
    """
    mock_run.return_value = None  # No exception => success
    result = Docker.Desktop.is_running()
    assert result is True
    mock_run.assert_called_once_with(
        ["docker", "info"],
        asynchronous=False,
        kwargs={"verbose": False}
    )

@patch("src.utils.command.Command.run")
def test_docker_desktop_is_running_false(mock_run):
    """
    If "docker info" raises an exception, Docker.Desktop.is_running() should return False.
    """
    mock_run.side_effect = Exception("Docker not running")
    result = Docker.Desktop.is_running()
    assert result is False

@patch("src.utils.command.Command.run")
def test_docker_desktop_start_already_running(mock_run):
    """
    If is_running() returns True, start() should do nothing additional.
    """
    with patch.object(Docker.Desktop, "is_running", return_value=True):
        Docker.Desktop.start()
        assert mock_run.call_count == 0

@patch("os.startfile")
@patch("src.utils.command.Command.run")
def test_docker_desktop_start_windows(mock_run, mock_startfile):
    """
    If on Windows and Docker not running, start() tries to open Docker Desktop.
    """
    with patch.object(Docker.Desktop, "is_running", return_value=False):
        with patch("platform.system", return_value="Windows"):
            Docker.Desktop.start()
            mock_startfile.assert_called()

@patch("platform.system", return_value="Linux")
@patch("os.path.exists", return_value=False)
def test_docker_desktop_start_non_windows(mock_exists, mock_platform):
    with patch("src.utils.docker.Docker.Desktop.is_running", return_value=False):
        Docker.Desktop.start()

@patch("src.utils.command.Command.run")
def test_docker_compose_build_npm(mock_run):
    with patch("platform.system", return_value="Windows"):
        Docker.Compose.build("my/frontend", npm=True, reinstall=True)
        assert mock_run.call_count >= 2
