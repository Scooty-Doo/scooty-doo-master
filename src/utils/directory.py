"""Module for handling directories in the project."""

import os
from .settings import Settings

class Directory:
    """Class for handling directories in the project."""
    @staticmethod
    def root():
        """Get the root directory of the project."""
        return os.getcwd()

    @staticmethod
    def database():
        """Get the database directory."""
        return os.path.join(Directory.Repo.backend(), Settings.Directory.Name.database)

    @staticmethod
    def mocked_data():
        """Get the mocked data directory."""
        return os.path.join(Directory.root(), Settings.Directory.mocked_data)

    @staticmethod
    def env():
        """Get the environment directory."""
        return os.path.join(Settings.Directory.env)

    @staticmethod
    def logs():
        """Get the logs directory."""
        return os.path.join(Directory.root(), Settings.Directory.logs)

    @staticmethod
    def env_example():
        """Get the example environment directory."""
        return os.path.join(Directory.env(), 'example')

    @staticmethod
    def venv(repo_dir):
        """Get the virtual environment directory."""
        return os.path.join(repo_dir, Settings.Directory.Name.venv)

    @staticmethod
    def docker_compose(repo_dir):
        """Get the Docker Compose file."""
        return os.path.join(repo_dir, 'docker-compose.yml')

    @staticmethod
    def repositories():
        """Get the repositories directory."""
        return os.path.join(Directory.root(), Settings.Directory.repositories)

    @staticmethod
    def local_repositories():
        """Get the local repositories directory."""
        return os.path.join(Directory.root(), Settings.Directory.local_repositories)

    class Repo:
        """Class for handling the repository directories."""
        @staticmethod
        def backend():
            """Get the backend repository directory."""
            return Directory.Repo.get(Settings.Directory.Name.backend)

        @staticmethod
        def frontend():
            """Get the frontend repository directory."""
            return Directory.Repo.get(Settings.Directory.Name.frontend)

        @staticmethod
        def bike():
            """Get the bike repository directory."""
            return Directory.Repo.get(Settings.Directory.Name.bike)

        @staticmethod
        def get(name):
            """Get a repository directory."""
            return os.path.join(Directory.root(), Settings.Directory.repositories, name)
