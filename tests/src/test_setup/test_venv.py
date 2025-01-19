# pylint: disable=protected-access
"""Module to test the setup of the virtual environment."""

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
    Test that _install_dependencies raises SystemExit if Dependencies.install fails.
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

@patch("src.setup._venv.Venv._build_venv")
@patch("src.setup._venv.Venv._install_dependencies")
def test_setup(mock_install_dependencies, mock_build_venv):
    """
    Test the setup method.
    """
    venv_path = "/fake/venv"
    Venv.setup(venv_path)
    mock_build_venv.assert_called_once_with(venv_path)
    mock_install_dependencies.assert_called_once_with(venv_path)

@patch("src.setup._venv.Venv.setup")
@patch("src.setup._venv.Directory.root", return_value="/fake/repo")
def test_setup_master(mock_directory_root, mock_setup):
    """
    Test the setup_master method.
    """
    Venv.setup_master()
    expected_venv_path = os.path.join("/fake/repo", "venv")
    mock_setup.assert_called_once_with(expected_venv_path)
    mock_directory_root.assert_called_once()

if __name__ == "__main__": # pragma: no cover
    Venv.setup_master()
