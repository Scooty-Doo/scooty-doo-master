import os
from src.utils.directory import Directory
from src.utils.settings import Settings

def test_root_is_cwd():
    assert Directory.root() == os.getcwd(), \
        "Directory.root() should return current working directory"

def test_mocked_data_path():
    expected = os.path.join(os.getcwd(), \
        "repos/backend/database/mock_data/data/generated/")
    assert Directory.mocked_data() == expected, "Should build the correct path to mocked data"

def test_env_directory():
    expected = os.path.join(Settings.Directory.env)
    assert Directory.env() == expected, \
        "Should build the correct path to 'env' directory"

def test_repo_backend():
    expected = os.path.join(os.getcwd(), \
        Settings.Directory.repositories, Settings.Directory.Name.backend)
    assert Directory.Repo.backend() == expected, "Should build the correct path to the backend repo"

def test_database_path():
    expected = os.path.join(os.getcwd(),
                            Settings.Directory.repositories,
                            Settings.Directory.Name.backend,
                            Settings.Directory.Name.database)
    assert Directory.database() == \
        expected, "Should build the correct path to the database directory"

def test_docker_compose_path():
    repo_dir = os.path.join(os.getcwd(), 'sample_repo')
    expected = os.path.join(repo_dir, 'docker-compose.yml')
    assert Directory.docker_compose(repo_dir) == \
        expected, "Should build the correct path to docker-compose.yml file"
