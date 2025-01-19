# pylint: disable=protected-access, broad-exception-caught
"""Module to manage the setup of the frontend server."""

import sys
from ._environment import Environment
from ..utils.directory import Directory
from ..utils.docker import Docker

ROOT_DIR = Directory.root()
REPO_DIR = Directory.Repo.frontend()

class Frontend:
    """
    Frontend class to manage the setup of the frontend instance.
    """
    @staticmethod
    def _env():
        """Setup the environment files."""
        Environment.Files.generate(frontend=True)

    class Docker:
        """Class to manage the Docker setup of the frontend server."""
        @staticmethod
        def _build():
            """Build the frontend Docker image."""
            print("Building the frontend Docker image...")
            try:
                Docker.Compose.build(REPO_DIR, npm=True, reinstall=True)
                print("Frontend Docker image built successfully.")
            except Exception as e:
                print(f"Failed to build the frontend Docker image: {e}")
                sys.exit(1)

        @staticmethod
        def _start():
            """Start the frontend Docker container."""
            try:
                Docker.Compose.up(REPO_DIR, npm=True)
                print("Frontend Docker container restarted successfully.")
            except Exception as e:
                print(f"Failed to restart the frontend Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def status():
            """Get the status of the frontend Docker container."""
            Docker.Compose.status(REPO_DIR)

        @staticmethod
        def logs():
            """Get the logs of the frontend Docker container."""
            Docker.Compose.logs(REPO_DIR)

    @staticmethod
    def setup():
        """Setup the frontend server."""
        Frontend._env()
        Frontend.Docker._build()

    @staticmethod
    def run():
        """Run the frontend server."""
        Frontend.Docker._start()
        Frontend.Docker.status()
        Frontend.Docker.logs()
        print("Hivemind Bike server started.")
