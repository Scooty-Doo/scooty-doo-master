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

@patch.object(Main, "_setup_backend")
@patch.object(Main, "_setup_bikes")
@patch.object(Main, "_setup_frontend")
@patch.object(Main, "_open_chrome_tabs")
def test_main_run(mock_open_chrome, mock_frontend, mock_bikes, mock_backend):
    main = Main(use_submodules=False)
    main.simulate(skip_setup=False, bikes=True, frontend=True, open_chrome_tabs=True, docker=True)

    mock_backend.assert_called_once_with(start_server=True, already_setup=False, docker=True)
    mock_bikes.assert_called_once()
    mock_frontend.assert_called_once()
    mock_open_chrome.assert_called_once()
