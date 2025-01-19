# pylint: disable=protected-access, broad-exception-caught

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
        @staticmethod
        def _build():
            try:
                print("Building the bike Docker image...")
                Docker.Compose.build(REPO_DIR)
            except Exception as e:
                print(f"Failed to build the bike Docker image: {e}")
                sys.exit(1)

        @staticmethod
        def _up():
            try:
                print("Starting the bike Docker container...")
                Docker.Compose.up(REPO_DIR)
            except Exception as e:
                print(f"Failed to start the bike Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _down():
            try:
                print("Stopping the bike Docker container...")
                Docker.Compose.down(REPO_DIR)
            except Exception as e:
                print(f"Failed to stop the bike Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _restart():
            Bike.Docker._down()
            Bike.Docker._up()

        @staticmethod
        def status():
            Docker.Compose.status(REPO_DIR)

        @staticmethod
        def logs():
            Docker.Compose.logs(REPO_DIR)

    @staticmethod
    def _venv():
        Venv.setup(VENV_DIR)

    @staticmethod
    def _env(bikes):
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
        if not docker:
            Bike._venv()
        if docker:
            Bike.Docker._build()
        Bike._env(bikes)

    @staticmethod
    def run():
        Bike._start_server()
        print("Hivemind Bike server started.")
