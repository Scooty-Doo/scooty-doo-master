from unittest.mock import patch
import pytest
from src.utils.dependencies import Dependencies
import subprocess

@patch("src.utils.dependencies.Command.run")
def test_dependencies_install_no_upgrade(mock_run):
    Dependencies.install("python", "/fake/repo", upgrade_pip=False)
    assert mock_run.call_count == 1

@patch("src.utils.dependencies.Command.run", \
       side_effect=subprocess.CalledProcessError(1, "pip upgrade"))
def test_dependencies_upgrade_fail(mock_run):
    """
    coverage for exception in Dependencies.Pip.upgrade
    """
    with pytest.raises(subprocess.CalledProcessError):
        Dependencies.install("python", "/fake/repo", upgrade_pip=True)
