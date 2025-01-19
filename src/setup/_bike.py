# pylint: disable=protected-access, broad-exception-caught
"""Module to manage the setup of the bike hivemind."""

import sys
from ._venv import Venv
from ._environment import Environment
from ..utils.directory import Directory
from ..utils.command import Command
from ..utils.docker import Docker

ROOT_DIR = Directory.root()
REPO_DIR = Directory.Repo.bike()
VENV_DIR = Directory.venv(REPO_DIR)
PYTHON_EXECUTABLE = Venv.get_python_executable(VENV_DIR)

class Bike:
    """
    Bike class to manage the setup of individual bike instances.
    """
    class Docker:
        """Class to manage the Docker setup of the bike hivemind."""
        @staticmethod
        def _build():
            """Build the bike Docker image."""
            try:
                print("Building the bike Docker image...")
                Docker.Compose.build(REPO_DIR)
            except Exception as e:
                print(f"Failed to build the bike Docker image: {e}")
                sys.exit(1)

        @staticmethod
        def _up():
            """Start the bike Docker container."""
            try:
                print("Starting the bike Docker container...")
                Docker.Compose.up(REPO_DIR)
            except Exception as e:
                print(f"Failed to start the bike Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _down():
            """Stop the bike Docker container."""
            try:
                print("Stopping the bike Docker container...")
                Docker.Compose.down(REPO_DIR)
            except Exception as e:
                print(f"Failed to stop the bike Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _restart():
            """Restart the bike Docker container."""
            Bike.Docker._down()
            Bike.Docker._up()

        @staticmethod
        def status():
            """Get the status of the bike Docker container."""
            Docker.Compose.status(REPO_DIR)

        @staticmethod
        def logs():
            """Get the logs of the bike Docker container."""
            Docker.Compose.logs(REPO_DIR)

    @staticmethod
    def _venv():
        """Setup the virtual environment for the bike hivemind."""
        Venv.setup(VENV_DIR)

    @staticmethod
    def _env(bikes):
        """Generate the .env file for the bike hivemind."""
        if not bikes:
            print("No bikes provided to generate .env file for.")
        Environment.Files.generate(bikes=bikes)

    @staticmethod
    def _start_server(docker=True):
        """
        Starts the FastAPI server for the bike hivemind.
        """
        print("Starting the FastAPI server for bike hivemind...")
        if docker:
            Bike.Docker._up()
            Bike.Docker.status()
            Bike.Docker.logs()
            return
        main_module = "src.main"
        try:
            Command.run(
                [PYTHON_EXECUTABLE, "-m", main_module],
                directory=REPO_DIR,
                stream_output=True
            )
            print("FastAPI server for the bike hivemind started successfully.")
        except Exception as e:
            print(f"Failed to start the FastAPI server for the bike hivemind: {e}")
            sys.exit(1)

    @staticmethod
    def setup(bikes, docker=True):
        """Setup the bike hivemind."""
        if not docker:
            Bike._venv()
        if docker:
            Bike.Docker._build()
        Bike._env(bikes)

    @staticmethod
    def run():
        """Run the bike hivemind."""
        Bike._start_server()
        print("Hivemind Bike server started.")
