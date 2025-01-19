"""Tests for the Dependencies class."""

import subprocess
from unittest.mock import patch
import pytest
from src.utils.dependencies import Dependencies

@patch("src.utils.dependencies.Command.run")
def test_dependencies_install_no_upgrade(mock_run):
    """Test installing dependencies without upgrading pip."""
    Dependencies.install("python", "/fake/repo", upgrade_pip=False)
    assert mock_run.call_count == 1

@patch("src.utils.dependencies.Command.run", \
       side_effect=subprocess.CalledProcessError(1, "pip upgrade"))
def test_dependencies_upgrade_fail(_mock_run):
    """Test upgrading dependencies failure."""
    with pytest.raises(subprocess.CalledProcessError):
        Dependencies.install("python", "/fake/repo", upgrade_pip=True)
