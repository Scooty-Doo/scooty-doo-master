from unittest.mock import patch
from src.utils.repositories import Repositories

@patch("src.utils.repositories._Local._Get._get_repository")
def test_repositories_local_all(mock_get_repo):
    r = Repositories()
    r.local.get.all(branch="my-branch")
    # Should call _get_repository 3 times: backend, frontend, bike
    assert mock_get_repo.call_count == 3
    # Check calls
    calls = [call_args[0][0] for call_args in mock_get_repo.call_args_list]
    assert calls == ["backend", "frontend", "bike"]
