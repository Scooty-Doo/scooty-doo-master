from unittest.mock import patch
from src.main import Main

@patch.object(Main, "_use_submodules")
@patch.object(Main, "_use_local_repositories")
def test_main_init_submodules_false(mock_local, mock_submodules):
    # If use_submodules=False, _use_local_repositories is called
    main = Main(use_submodules=False)
    mock_local.assert_called_once()
    mock_submodules.assert_not_called()

@patch.object(Main, "_use_submodules")
@patch.object(Main, "_use_local_repositories")
def test_main_init_submodules_true(mock_local, mock_submodules):
    # If use_submodules=True, _use_submodules is called
    main = Main(use_submodules=True)
    mock_submodules.assert_called_once()
    mock_local.assert_not_called()
