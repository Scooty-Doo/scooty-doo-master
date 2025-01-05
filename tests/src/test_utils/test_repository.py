import pytest
from unittest.mock import patch
from src.utils.repository import Repository

@patch("src.utils.command.Command.run")
def test_repository_fetch(mock_run):
    Repository.fetch("/path/to/repo")
    mock_run.assert_called_once_with(["git", "-C", "/path/to/repo", "fetch"], raise_exception=True)

@patch("src.utils.command.Command.run")
def test_repository_checkout(mock_run):
    Repository.checkout("/path/to/repo", "development")
    mock_run.assert_called_once_with(["git", "-C", "/path/to/repo", "checkout", "development"], raise_exception=True)

@patch("src.utils.command.Command.run")
def test_repository_pull_no_force(mock_run):
    Repository.pull("/path/to/repo", force=False, branch=None)
    mock_run.assert_called_once()  # calling "_pull()"
    args = mock_run.call_args[0][0]
    assert args == ["git", "-C", "/path/to/repo", "pull"]

@patch("src.utils.command.Command.run")
def test_repository_clone(mock_run):
    Repository.clone("https://myrepo.git", "/some/local/path", branch="main")
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["git", "clone", "https://myrepo.git", "/some/local/path", "-b", "main"]

def test_checkout_files_no_files(capfd):
    """
    If the 'files' list is empty, it prints 'No files to checkout.' and returns.
    """
    Repository.Checkout.files("/fake/repo", [])
    captured = capfd.readouterr()
    assert "No files to checkout." in captured.out

@patch("src.utils.command.Command.run")
def test_checkout_files_success(mock_run, capfd):
    """
    If files are provided, Command.run should be called, and success message printed.
    """
    Repository.Checkout.files("/fake/repo", ["file1.txt", "file2.txt"])
    mock_run.assert_called_once_with(
        ["git", "-C", "/fake/repo", "checkout", "--", "file1.txt", "file2.txt"],
        raise_exception=True
    )
    captured = capfd.readouterr()
    assert "Successfully checked out files: ['file1.txt', 'file2.txt']" in captured.out

@patch("src.utils.command.Command.run", side_effect=Exception("Checkout error"))
def test_checkout_files_exception(mock_run, capfd):
    """
    If Command.run raises an exception, it should catch it, print the error, and re-raise.
    """
    with pytest.raises(Exception) as exc:
        Repository.Checkout.files("/fake/repo", ["some_file.txt"])
    captured = capfd.readouterr()
    assert "Error checking out files ['some_file.txt']:" in captured.out
    assert "Checkout error" in str(exc.value)
