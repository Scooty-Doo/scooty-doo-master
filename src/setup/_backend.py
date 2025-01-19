# pylint: disable=protected-access, broad-exception-caught, too-few-public-methods
"""Module to manage the setup of the backend server."""

import sys
import os
from ..utils.docker import Docker
from ..utils.directory import Directory

REPO_DIR = Directory.Repo.backend()
DATABASE_CONTAINER = os.getenv("DATABASE_CONTAINER", 'database-db-1')
DATABASE_ADMINER_CONTAINER = os.getenv("DATABASE_ADMINER_CONTAINER", 'database-adminer-1')
BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER", 'api')

class Backend:
    """
    Backend class to manage the setup of the backend server.
    """
    class Docker:
        """Class to manage the Docker setup of the backend server."""
        @staticmethod
        def _build():
            """Build the backend Docker image."""
            try:
                print("Building the backend Docker image...")
                Docker.Compose.build(REPO_DIR)
            except Exception as e:
                print(f"Failed to build the backend Docker image: {e}")
                sys.exit(1)

        @staticmethod
        def _up():
            """Start the backend Docker container."""
            try:
                print("Starting the backend Docker container...")
                Docker.Compose.up(REPO_DIR)
            except Exception as e:
                print(f"Failed to start the backend Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _down():
            """Stop the backend Docker container."""
            try:
                print("Stopping the backend Docker container...")
                Docker.Compose.down(REPO_DIR)
            except Exception as e:
                print(f"Failed to stop the backend Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _restart():
            """Restart the backend Docker container."""
            Backend.Docker._down()
            Backend.Docker._up()

        @staticmethod
        def status():
            """Get the status of the backend Docker container."""
            Docker.Compose.status(REPO_DIR)

        @staticmethod
        def logs():
            """Get the logs of the backend Docker container."""
            Docker.Compose.logs(REPO_DIR)

        @staticmethod
        def _clear():
            """Clear the backend Docker container."""
            Docker.Container.delete(DATABASE_CONTAINER)
            Docker.Container.delete(DATABASE_ADMINER_CONTAINER)
            Docker.Container.delete(BACKEND_CONTAINER)

    @staticmethod
    def _setup():
        """Setup the backend server."""
        Backend.Docker._down()
        Backend.Docker._clear()
        Backend.Docker._build()
        Backend.Docker._up()
        Backend.Docker.status()
        Backend.Docker.logs()

    @staticmethod
    def run():
        """Run the backend server."""
        Backend._setup()
