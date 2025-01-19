"""Tests for Chrome class."""

from unittest.mock import patch
from src.utils.chrome import Chrome

@patch("src.utils.command.Command.run")
def test_chrome_open_no_ports(mock_command_run):
    """Test opening Chrome with no ports."""
    with patch("src.utils.chrome.IS_WINDOWS", True):
        Chrome.Open.window()
        mock_command_run.assert_called_once()
        assert "chrome.exe" in mock_command_run.call_args[0][0][0].lower()

@patch("src.utils.command.Command.run")
def test_chrome_open_with_ports(mock_command_run):
    """Test opening Chrome with ports."""
    with patch("src.utils.chrome.IS_WINDOWS", True):
        Chrome.Open.window("8000/docs", "8001/docs")
        assert mock_command_run.call_count == 1
        args = mock_command_run.call_args[0][0]
        assert "--new-tab" in args
        assert "http://localhost:8000/docs" in args
        assert "http://localhost:8001/docs" in args

@patch("builtins.print")
def test_chrome_open_non_windows(mock_print):
    """Test opening Chrome on non-Windows platforms."""
    with patch("src.utils.chrome.IS_WINDOWS", False):
        Chrome.Open.window("8000")
        mock_print.assert_called_once_with("If not on Windows, please open Chrome window manually.")
