# pylint: disable=protected-access

import subprocess
import os
from unittest.mock import patch
import pytest
from src.setup._venv import Venv

@patch("src.setup._venv.os.path.exists", return_value=False)
@patch("src.setup._venv.Command.run")
def test_build_venv_not_exists(mock_command_run, _mock_exists):
    """
    If the venv folder does not exist, _build_venv should create it (via Command.run).
    """
    Venv._build_venv("/fake/venv")
    mock_command_run.assert_called_once()
    assert "venv" in mock_command_run.call_args[0][0]

@patch("src.setup._venv.os.path.exists", return_value=True)
@patch("src.setup._venv.Command.run")
def test_build_venv_already_exists(mock_command_run, _mock_exists):
    """
    If the venv folder exists, _build_venv prints message and does not call Command.run.
    """
    Venv._build_venv("/fake/venv")
    mock_command_run.assert_not_called()

@patch("src.setup._venv.Dependencies.install")
def test_install_dependencies(mock_install):
    """
    Should call Dependencies.install with correct python_executable path.
    """
    Venv._install_dependencies("/fake/venv")
    mock_install.assert_called_once()
    (python_executable, repo_dir) = mock_install.call_args[0][0:2]
    assert (python_executable.endswith("python.exe") or python_executable.endswith("python"))
    assert repo_dir == "/fake"

@patch("src.setup._venv.Dependencies.install",
       side_effect=subprocess.CalledProcessError(1, "pip install"))
def test_install_dependencies_fail(_mock_install):
    """
    coverage for an exception in _install_dependencies
    """
    with pytest.raises(SystemExit) as exc_info:
        Venv._install_dependencies("/fake/venv")
    assert exc_info.value.code == 1

def test_get_python_executable_non_windows():
    """
    Test get_python_executable function for non-Windows platforms.
    """
    with patch("src.setup._venv.IS_WINDOWS", False):
        venv_path = "/fake/venv"
        expected_path = os.path.join(venv_path, "bin", "python")
        assert Venv.get_python_executable(venv_path) == expected_path

if __name__ == "__main__": # pragma: no cover
    Venv.setup_master()
