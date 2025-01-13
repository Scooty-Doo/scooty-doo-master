import subprocess
from unittest.mock import patch
import pytest
from src.utils.command import Command

def test_run_synchronous_raise_exception():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
        Command.run(
            ["echo", "hello"],
            asynchronous=False,
            raise_exception=True,
            stream_output=False
            )
        mock_run.assert_called_once()

def test_run_asynchronous_no_exception():
    with patch("subprocess.Popen") as mock_popen:
        Command.run(["echo", "hello"], asynchronous=True, raise_exception=False)
        mock_popen.assert_called_once()

def test_run_command_fails():
    with patch("subprocess.check_call", \
               side_effect=subprocess.CalledProcessError(1, "cmd")):
        with pytest.raises(SystemExit):
            Command.run(["failing_cmd"], asynchronous=True, raise_exception=True)
