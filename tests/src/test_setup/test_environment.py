# pylint: disable=protected-access, undefined-variable
"""Module to test the setup of the environment files."""

from unittest.mock import patch
import pytest
from src.setup._environment import Environment

@patch("src.setup._environment.Environment._copy_env_file")
def test_environment_files_generate(mock_copy_env_file):
    """Test the environment files generation."""
    Environment.Files.generate(backend=True, frontend=True, bikes=False)
    assert mock_copy_env_file.call_count == 2

@patch("src.setup._environment.Environment._copy_env_file")
def test_environment_files_generate_none(mock_copy_env_file):
    """Test the environment files generation with no arguments."""
    Environment.Files.generate(backend=False, frontend=False, bikes=False)
    mock_copy_env_file.assert_not_called()

@patch("src.setup._environment.shutil.copyfile")
@patch("src.setup._environment.os.path.exists", return_value=True)
def test_environment_copy_env_file(_mock_exists, mock_copyfile):
    """Test the environment file copy operation."""
    Environment._copy_env_file('.env.backend', 'backend_path')
    mock_copyfile.assert_called_once()

@patch("src.setup._environment.os.path.exists", return_value=False)
def test_environment_copy_env_file_source_missing(_mock_exists):
    """Test the environment file copy operation with a missing source file."""
    with pytest.raises(FileNotFoundError):
        Environment._copy_env_file('.env.missing', 'backend_path')

@patch("src.setup._environment.shutil.copyfile")
@patch("src.setup._environment.os.path.exists",
       side_effect=lambda path: not 'env' in path)
def test_environment_root_env_missing(_mock_exists, _mock_copyfile):
    """Test the root environment file copy operation with a missing source file."""
    with pytest.raises(FileNotFoundError):
        Environment.Files._setup()

@patch("src.setup._environment.os.path.exists",
       side_effect=lambda path: not 'missing_repo' in path)
def test_environment_copy_env_file_target_missing(_mock_exists):
    """Test the environment file copy operation with a missing target file."""
    with pytest.raises(FileNotFoundError):
        Environment._copy_env_file('.env.backend', 'missing_repo')
