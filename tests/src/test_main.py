from unittest.mock import patch
from src.main import Main

@patch.object(Main, "_use_submodules")
@patch.object(Main, "_use_local_repositories")
def test_main_init_submodules_false(mock_local, mock_submodules):
    _ = Main(use_submodules=False)
    mock_local.assert_called_once()
    mock_submodules.assert_not_called()

@patch.object(Main, "_use_submodules")
@patch.object(Main, "_use_local_repositories")
def test_main_init_submodules_true(mock_local, mock_submodules):
    _ = Main(use_submodules=True)
    mock_submodules.assert_called_once()
    mock_local.assert_not_called()

@patch("src.main.Get")
@patch("src.main.Repositories")
def test_main_init(mock_repositories, mock_get):
    _ = Main(use_submodules=False)
    mock_get.assert_called_once()
    mock_repositories.assert_called_once()

@patch("src.main.Setup.master")
def test_main_setup_master(mock_setup):
    main = Main()
    main._setup_master(simulation=True, rebuild=True)
    mock_setup.assert_called_once_with(True, True)

# @patch("src.main.Chrome.Open.window")
# @patch("src.main.platform.system", return_value="Windows")
# def test_main_open_chrome_tabs(mock_platform, mock_chrome):
#     main = Main()
#     main._open_chrome_tabs()
#     mock_chrome.assert_called()
#     mock_platform.assert_called()

@patch("src.main.Main._run")
def test_main_simulate(mock_run):
    main = Main()
    main.simulate(simulation_speed_factor=2.0, open_chrome_tabs=False, rebuild=True, bike_limit=100)
    mock_run.assert_called_once()

# @patch("src.main.os.environ")
# def test_main_use_local_repositories(mock_environ):
#     _ = Main(use_submodules=False)
#     assert mock_environ.__setitem__.called

@patch("src.main.Chrome.Open.window")
@patch("src.main.platform.system")
def test_main_open_chrome_tabs_windows(mock_system, mock_chrome_open):
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
    mock_system.return_value = "Linux"
    main = Main()
    main._open_chrome_tabs(bikes=True, frontend=True)
    mock_chrome_open.assert_not_called()

@patch("src.main.Main._run")
def test_main_run_public(mock_run):
    main = Main()
    main.run(simulation_speed_factor=1.0, open_chrome_tabs=True, rebuild=False, bike_limit=9999)
    mock_run.assert_called_once_with(
        simulation=False,
        simulation_speed_factor=1.0,
        rebuild=False,
        open_chrome_tabs=True,
        bike_limit=9999
    )
