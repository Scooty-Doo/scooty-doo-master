import sys
from ._venv import Venv
from ._environment import Environment
from ..utils.directory import Directory
from ..utils.command import Command

ROOT_DIR = Directory.root()
REPO_DIR = Directory.Repo.bike()
VENV_DIR = Directory.venv(REPO_DIR)
PYTHON_EXECUTABLE = Venv.get_python_executable(VENV_DIR)

class Bike:
    """
    Bike class to manage the setup of individual bike instances.
    """
    @staticmethod
    def _venv():
        Venv.setup(VENV_DIR)

    @staticmethod
    def _env(bikes):
        if not bikes:
            print("No bikes provided to generate .env file for.")
        Environment.Files.generate(bikes=bikes)
    
    @staticmethod
    def _start_server():
        """
        Starts the FastAPI server for the bike hivemind.
        """
        print("Starting the FastAPI server for bike hivemind...")
        MAIN_MODULE = "src.main"
        try:
            Command.run(
                [PYTHON_EXECUTABLE, "-m", MAIN_MODULE],
                directory=REPO_DIR,
                stream_output=True
            )
            print("FastAPI server for the bike hivemind started successfully.")
        except Exception as e:
            print(f"Failed to start the FastAPI server for the bike hivemind: {e}")
            sys.exit(1)

    @staticmethod
    def setup(bikes):
        Bike._venv()
        Bike._env(bikes)
    
    @staticmethod
    def run():
        Bike._start_server()
        print("Hivemind Bike server started.")

if __name__ == "__main__":
    bike = Bike()
    bike.setup()

# python -m src.setup._bike

# TODO: Arrange a Docker setup for bike repo.
