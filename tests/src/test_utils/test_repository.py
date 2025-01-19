"""Tests for the Repository class."""

from unittest.mock import patch
import pytest
from src.utils.repository import Repository

@patch("src.utils.command.Command.run")
def test_repository_fetch(mock_run):
    """Test fetching a repository."""
    Repository.fetch("/path/to/repo")
    mock_run.assert_called_once_with(["git", "-C", "/path/to/repo", "fetch"], raise_exception=True)

@patch("src.utils.command.Command.run")
def test_repository_checkout(mock_run):
    """Test checking out a repository."""
    Repository.checkout("/path/to/repo", "development")
    mock_run.assert_called_once_with(
        ["git", "-C", "/path/to/repo", "checkout", "development"],
        raise_exception=True)

@patch("src.utils.command.Command.run")
def test_repository_pull_no_force(mock_run):
    """Test pulling a repository without force."""
    Repository.pull("/path/to/repo", force=False, branch=None)
    mock_run.assert_called_once()  # calling "_pull()"
    args = mock_run.call_args[0][0]
    assert args == ["git", "-C", "/path/to/repo", "pull"]

@patch("src.utils.command.Command.run")
def test_repository_clone(mock_run):
    """Test cloning a repository."""
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
def test_checkout_files_exception(_mock_run, capfd):
    """
    If Command.run raises an exception, it should catch it, print the error, and re-raise.
    """
    with pytest.raises(Exception) as exc:
        Repository.Checkout.files("/fake/repo", ["some_file.txt"])
    captured = capfd.readouterr()
    assert "Error checking out files ['some_file.txt']:" in captured.out
    assert "Checkout error" in str(exc.value)

@patch("src.utils.command.Command.run")
def test_repository_pull_with_commit(mock_run, capfd):
    """Test pulling a repository with a specific commit."""
    Repository.pull("/path/to/repo", force=False, commit="abc123")
    assert mock_run.call_count == 2
    args_pull = mock_run.call_args_list[0][0][0]
    args_reset = mock_run.call_args_list[1][0][0]
    assert args_pull == ["git", "-C", "/path/to/repo", "pull"]
    assert args_reset == ["git", "-C", "/path/to/repo", "reset", "--hard", "abc123"]
    captured = capfd.readouterr()
    assert "Resetting repository /path/to/repo to commit abc123..." in captured.out

@patch("src.utils.command.Command.run")
def test_repository_pull_with_force(mock_run):
    """Test pulling a repository with force."""
    Repository.pull("/path/to/repo", force=True)
    assert mock_run.call_count == 2
    args_checkout = mock_run.call_args_list[0][0][0]
    args_pull = mock_run.call_args_list[1][0][0]
    assert args_checkout == ["git", "-C", "/path/to/repo",
                             "checkout", "--",
                             "package.json", "package-lock.json"]
    assert args_pull == ["git", "-C", "/path/to/repo", "pull"]

@patch("src.utils.command.Command.run")
def test_repository_pull_with_force_and_commit(mock_run, capfd):
    """Test pulling a repository with force and a specific commit."""
    Repository.pull("/path/to/repo", force=True, commit="xyz789")
    assert mock_run.call_count == 3
    args_checkout = mock_run.call_args_list[0][0][0]
    args_pull = mock_run.call_args_list[1][0][0]
    args_reset = mock_run.call_args_list[2][0][0]
    assert args_checkout == ["git", "-C", "/path/to/repo",
                             "checkout", "--", "package.json",
                             "package-lock.json"]
    assert args_pull == ["git", "-C", "/path/to/repo", "pull"]
    assert args_reset == ["git", "-C", "/path/to/repo", "reset", "--hard", "xyz789"]
    captured = capfd.readouterr()
    assert "Resetting repository /path/to/repo to commit xyz789..." in captured.out

@patch("src.utils.command.Command.run")
def test_repository_print_commit_success(mock_run, capfd):
    """Test printing the latest commit."""
    mock_run.return_value = "a1b2c3 - Fixing bug"
    Repository.Print.commit("/path/to/repo")
    mock_run.assert_called_once_with([
        "git", "-C", "/path/to/repo", "log", "-1", "--pretty=format:%h - %s"
    ], raise_exception=True)
    captured = capfd.readouterr()
    assert "Commit after pull in /path/to/repo: a1b2c3 - Fixing bug" in captured.out

@patch("src.utils.command.Command.run", side_effect=Exception("Log error"))
def test_repository_print_commit_exception(_mock_run, capfd):
    """Test printing the latest commit with an exception."""
    Repository.Print.commit("/path/to/repo")
    captured = capfd.readouterr()
    assert "Error retrieving commit info after pull: Log error" in captured.out
