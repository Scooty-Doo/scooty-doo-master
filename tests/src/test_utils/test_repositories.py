from unittest.mock import patch
import pytest
from src.utils.repositories import Repositories

@patch("src.utils.repositories.os.makedirs")
@patch("src.utils.repositories.Repository.clone")
@patch("src.utils.repositories.Repository.checkout")
@patch("src.utils.repositories.Repository.pull")
@patch("src.utils.repositories.Repository.Print.commit")
def test_local_get_backend(mock_commit, mock_pull, mock_checkout, _mock_clone, _mock_makedirs):
    repos = Repositories()
    repos.local.get.backend(branch="main", commit="12345")
    mock_checkout.assert_called_once()
    mock_pull.assert_called_once()
    mock_commit.assert_called_once()

@patch("src.utils.repositories.Repository.clone")
@patch("src.utils.repositories.Repository.checkout")
@patch("src.utils.repositories.Repository.pull")
@patch("src.utils.repositories.Repository.Print.commit")
def test_local_get_all(mock_commit, mock_pull, mock_checkout, mock_clone):
    repos = Repositories()
    repos.local.get.all(branch="main")
    assert mock_clone.call_count == 0
    assert mock_checkout.call_count == 3
    assert mock_pull.call_count == 3
    assert mock_commit.call_count == 6

@patch("src.utils.repositories.Command.run")
def test_submodules_get_all(mock_run):
    repos = Repositories()
    repos.submodules.get.all()
    assert mock_run.call_count == 2

@patch("src.utils.repositories.Command.run")
def test_submodules_deinitialize_all(mock_run):
    repos = Repositories()
    repos.submodules.deinitialize.all()
    mock_run.assert_called_once()

@patch("src.utils.repositories.Repository.clone")
@patch("src.utils.repositories.os.path.isdir", return_value=True)
def test_local_get_repository_exists(_mock_isdir, mock_clone):
    repos = Repositories()
    repos.local.get.backend(branch="main")
    mock_clone.assert_not_called()

def test_local_get_repository_not_exists_clone():
    with patch("src.utils.repositories.os.path.isdir", return_value=False), \
         patch("src.utils.repositories.os.makedirs"), \
         patch("src.utils.repositories.Repository.clone") as mock_clone, \
         patch("src.utils.repositories.Repository.checkout") as mock_checkout, \
         patch("src.utils.repositories.Repository.pull") as mock_pull, \
         patch("src.utils.repositories.Repository.Print.commit") as mock_commit:
        repos = Repositories()
        repos.local.get.backend(branch="main", commit="12345")
        mock_clone.assert_called_once()
        mock_checkout.assert_called_once()
        mock_pull.assert_called_once()
        mock_commit.assert_called_once()

def test_local_get_repository_not_exists_no_branch():
    with patch("src.utils.repositories.os.path.isdir", return_value=False), \
         patch("src.utils.repositories.os.makedirs"), \
         patch("src.utils.repositories.Repository.clone") as mock_clone, \
         patch("src.utils.repositories.Repository.checkout") as mock_checkout, \
         patch("src.utils.repositories.Repository.pull") as mock_pull, \
         patch("src.utils.repositories.Repository.Print.commit") as mock_commit:
        repos = Repositories()
        repos.local.get.backend()
        mock_clone.assert_called_once()
        mock_checkout.assert_not_called()
        mock_pull.assert_not_called()
        mock_commit.assert_called_once()

def test_local_get_repository_not_exists_with_commit():
    with patch("src.utils.repositories.os.path.isdir", return_value=False), \
         patch("src.utils.repositories.os.makedirs"), \
         patch("src.utils.repositories.Repository.clone") as mock_clone, \
         patch("src.utils.repositories.Repository.pull") as mock_pull, \
         patch("src.utils.repositories.Repository.Print.commit") as mock_commit:
        repos = Repositories()
        repos.local.get.backend(commit="67890")
        mock_clone.assert_called_once()
        mock_pull.assert_called_once()
        mock_commit.assert_called_once()

def test_local_get_repository_exists_with_commit():
    with patch("src.utils.repositories.os.path.isdir", return_value=True), \
         patch("src.utils.repositories.os.path.join", return_value="/mocked/path/backend"), \
         patch("src.utils.repositories.Repository.pull") as mock_pull, \
         patch("src.utils.repositories.Repository.Print.commit") as mock_commit:
        repos = Repositories()
        repos.local.get.backend(commit="67890")
        mock_pull.assert_called_once_with("/mocked/path/backend", force=False, commit="67890")
        mock_commit.assert_called_once()

def test_local_get_repository_exists_without_commit():
    with patch("src.utils.repositories.os.path.isdir", return_value=True), \
         patch("src.utils.repositories.os.path.join", return_value="/mocked/path/backend"), \
         patch("src.utils.repositories.Repository.pull") as mock_pull, \
         patch("src.utils.repositories.Repository.Print.commit") as mock_commit:
        repos = Repositories()
        repos.local.get.backend()
        mock_pull.assert_called_once_with("/mocked/path/backend", force=False)
        mock_commit.assert_called_once()

def test_local_get_unknown_repository():
    repos = Repositories()
    with pytest.raises(ValueError, match="Unknown repository: unknown_repo"):
        repos.local.get._get_repository("unknown_repo")
