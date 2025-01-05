from unittest.mock import patch
from src.utils.chrome import Chrome

@patch("src.utils.command.Command.run")
def test_chrome_open_no_ports(mock_command_run):
    """
    If Chrome.Open.window() is called with no ports on Windows,
    it should call Command.run once (with only the chrome executable).
    """
    # Force Windows path so the code tries to run chrome
    with patch("platform.system", return_value="Windows"):
        Chrome.Open.window()  # no ports
        mock_command_run.assert_called_once()
        assert "chrome.exe" in mock_command_run.call_args[0][0][0].lower()

@patch("src.utils.command.Command.run")
def test_chrome_open_with_ports(mock_command_run):
    """
    If Chrome.Open.window() is called with ports, verify calls.
    """
    with patch("platform.system", return_value="Windows"):
        Chrome.Open.window("8000/docs", "8001/docs")
        assert mock_command_run.call_count == 1
        args = mock_command_run.call_args[0][0]
        # e.g. ["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", "--new-tab", "http://localhost:8000/docs", "http://localhost:8001/docs"]
        assert "--new-tab" in args
        # Check that the URLs got appended
        assert "http://localhost:8000/docs" in args
        assert "http://localhost:8001/docs" in args
