# pylint: disable=protected-access, disable=no-name-in-module
"""Tests for the Main class."""

import os
from unittest.mock import patch, MagicMock, call
import pytest
from src.main import Main

@pytest.fixture
def clean_environ():
    """Fixture to clean the environment after each test."""
    old_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(old_env)

@patch.object(Main, "_use_submodules")
@patch.object(Main, "_use_local_repositories")
def test_main_init_submodules_false(mock_local, mock_submodules):
    """Test initializing Main with use_submodules=False."""
    _ = Main(use_submodules=False)
    mock_local.assert_called_once()
    mock_submodules.assert_not_called()

@patch.object(Main, "_use_submodules")
@patch.object(Main, "_use_local_repositories")
def test_main_init_submodules_true(mock_local, mock_submodules):
    """Test initializing Main with use_submodules=True."""
    _ = Main(use_submodules=True)
    mock_submodules.assert_called_once()
    mock_local.assert_not_called()

@patch("src.main.Get")
@patch("src.main.Repositories")
def test_main_init(mock_repositories, mock_get):
    """Test initializing Main."""
    _ = Main(use_submodules=False)
    mock_get.assert_called_once()
    mock_repositories.assert_called_once()

@patch("src.main.Setup.master")
def test_main_setup_master(mock_setup):
    """Test setting up the master repository."""
    main = Main()
    main._setup_master(simulation=True, rebuild=True)
    mock_setup.assert_called_once_with(True, True)

@patch("src.main.Main._run")
def test_main_simulate(mock_run):
    """Test simulating the system."""
    main = Main()
    main.simulate(simulation_speed_factor=2.0, open_chrome_tabs=False, rebuild=True, bike_limit=100)
    mock_run.assert_called_once()

@patch("src.main.Chrome.Open.window")
@patch("src.main.platform.system")
def test_main_open_chrome_tabs_windows(mock_system, mock_chrome_open):
    """Test opening Chrome tabs on Windows."""
    mock_system.return_value = "Windows"
    with patch.dict('os.environ', {
        "BACKEND_PORT": "8000",
        "BIKES_PORT": "8001",
        "FRONTEND_PORT": "3000"
    }):
        main = Main()
        main._open_chrome_tabs(bikes=True, frontend=True)
        mock_chrome_open.assert_called_once_with("8000/docs", "8001/docs", "3000")

@patch("src.main.Chrome.Open.window")
@patch("src.main.platform.system")
def test_main_open_chrome_tabs_non_windows(mock_system, mock_chrome_open):
    """Test opening Chrome tabs on non-Windows platforms."""
    mock_system.return_value = "Linux"
    main = Main()
    main._open_chrome_tabs(bikes=True, frontend=True)
    mock_chrome_open.assert_not_called()

@patch("src.main.Main._run")
def test_main_run(mock_run):
    """Test running the system."""
    main = Main()
    main.run(simulation_speed_factor=1.0, open_chrome_tabs=True, rebuild=False, bike_limit=9999)
    mock_run.assert_called_once_with(
        simulation=False,
        simulation_speed_factor=1.0,
        rebuild=False,
        open_chrome_tabs=True,
        bike_limit=9999
    )

### USE SUBMODULES METHOD ###

@pytest.mark.usefixtures("clean_environ")
class TestUseSubmodules:
    """Tests for the _use_submodules method."""
    @patch("src.main.Settings.Directory.Name.submodules", new="fake_submodules_dir")
    @patch.object(Main, "__init__", return_value=None)
    def test_use_submodules_auto_pull_true(self, _mock_init):
        """Test _use_submodules with auto_pull=True."""
        main = Main()
        main.repositories = MagicMock()
        main._use_submodules(auto_pull=True)
        assert os.environ["REPOSITORIES_DIRECTORY"] == "fake_submodules_dir"
        main.repositories.submodules.get.all.assert_called_once()

    @patch("src.main.Settings.Directory.Name.submodules", new="fake_submodules_dir")
    @patch.object(Main, "__init__", return_value=None)
    def test_use_submodules_auto_pull_false(self, _mock_init):
        """Test _use_submodules with auto_pull=False."""
        main = Main()
        main.repositories = MagicMock()
        main._use_submodules(auto_pull=False)
        assert os.environ["REPOSITORIES_DIRECTORY"] == "fake_submodules_dir"
        main.repositories.submodules.get.all.assert_not_called()

### RUN METHOD ###

@pytest.mark.usefixtures("clean_environ")
class TestRunMethod:
    """Tests for the _run method."""
    @pytest.fixture(autouse=True)
    def setup_env(self):
        """Fixture to set the environment variables."""
        os.environ["BIKE_CONTAINER"] = "bike_hivemind"
        os.environ["SIMULATION_CONTAINER"] = "simulation"
        yield

    @patch("src.main.Main._setup_master")
    @patch("src.main.Main._open_chrome_tabs")
    @patch("src.main.Docker.Compose.Environment.reset")
    @patch("src.main.Docker.Compose.Environment.set")
    def test_run_default(
        self, mock_env_set, mock_env_reset, mock_open_tabs, mock_setup_master
    ):
        """Test running the system with default parameters."""
        main = Main(use_submodules=False)
        main._run()
        assert mock_env_reset.call_count == 2
        mock_env_reset.assert_any_call(simulation=False)
        mock_env_reset.assert_any_call(simulation=True)
        mock_env_set.assert_not_called()
        mock_setup_master.assert_called_once_with(True, False)
        mock_open_tabs.assert_not_called()

    @patch("src.main.Main._setup_master")
    @patch("src.main.Main._open_chrome_tabs")
    @patch("src.main.Docker.Compose.Environment.reset")
    @patch("src.main.Docker.Compose.Environment.set")
    def test_run_custom_speed_and_bike_limit(
        self, mock_env_set, mock_env_reset, mock_open_tabs, mock_setup_master):
        """Test running the system with custom speed and bike limit."""
        main = Main(use_submodules=False)
        main._run(simulation_speed_factor=2.0, bike_limit=100)
        mock_env_reset.assert_not_called()
        expected_calls = [
            call("bike_hivemind", "DEFAULT_SPEED", 40),
            call("bike_hivemind", "BIKE_LIMIT", 100),
            call("simulation", "BIKE_LIMIT", 100),
        ]
        assert mock_env_set.call_count == 3
        mock_env_set.assert_has_calls(expected_calls, any_order=True)
        mock_setup_master.assert_called_once_with(True, False)
        mock_open_tabs.assert_not_called()

    @patch("src.main.Main._setup_master")
    @patch("src.main.Main._open_chrome_tabs")
    @patch("src.main.Docker.Compose.Environment.reset")
    @patch("src.main.Docker.Compose.Environment.set")
    def test_run_open_chrome_tabs(
        self, mock_env_set, mock_env_reset, mock_open_tabs, mock_setup_master):
        """Test running the system with open_chrome_tabs=True."""
        main = Main(use_submodules=False)
        main._run(open_chrome_tabs=True)
        assert mock_env_reset.call_count == 2
        mock_env_set.assert_not_called()
        mock_setup_master.assert_called_once_with(True, False)
        mock_open_tabs.assert_called_once_with(bikes=True, frontend=True)
