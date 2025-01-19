import subprocess
import sys
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

def test_run_inherit_environment():
    with patch("subprocess.run") as mock_run:
        Command.run(
            ["echo", "hello"],
            inherit_environment=True,
            asynchronous=False, raise_exception=True)
        mock_run.assert_called_once_with(
            ["echo", "hello"],
            cwd=None,
            check=True,
            stdout=None,
            stderr=None,
            env=None
        )

def test_run_failing_command_no_exception():
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "echo")):
        try:
            Command.run(["echo", "hello"], asynchronous=False, raise_exception=False)
        except SystemExit:
            pytest.fail("SystemExit should not be raised when raise_exception is False")

def test_run_failing_command_with_exception():
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "echo")):
        with pytest.raises(SystemExit):
            Command.run(["echo", "hello"], asynchronous=False, raise_exception=True)

def test_run_synchronous_no_exception():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0)
        Command.run(["echo", "hello"], asynchronous=False, raise_exception=False)
        mock_run.assert_called_once_with(
            ["echo", "hello"],
            cwd=None,
            check=False,
            stdout=None,
            stderr=None,
            env=None
        )

def test_run_with_stream_output():
    with patch("subprocess.run") as mock_run:
        Command.run(
            ["echo", "hello"],
            asynchronous=False,
            raise_exception=True,
            stream_output=True
        )
        mock_run.assert_called_once_with(
            ["echo", "hello"],
            cwd=None,
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            env=None
        )

def test_run_with_return_output():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout=b"output", stderr=b"")
        Command.run(
            ["echo", "hello"],
            asynchronous=False,
            raise_exception=True,
            return_output=True
        )
        mock_run.assert_called_once_with(
            ["echo", "hello"],
            cwd=None,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=None
        )
