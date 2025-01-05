from unittest.mock import patch
from src.setup._environment import Environment

@patch("shutil.copyfile")
@patch("os.path.exists", side_effect=lambda path: True)  # pretend files exist
def test_copy_env_file(mock_exists, mock_copy):
    """
    _copy_env_file should copy from source_env_filename to target_repo's .env file
    """
    Environment._copy_env_file(".env.backend", "backend")
    mock_copy.assert_called_once()
