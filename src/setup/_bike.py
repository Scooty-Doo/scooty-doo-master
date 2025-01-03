from ._venv import Venv
from ._environment import Environment
from ..utils.directory import Directory
from ..data.get import Get

ROOT_DIR = Directory.root()
REPO_DIR = Directory.Repo.bike()
VENV_DIR = Directory.venv(REPO_DIR)

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
    def _start_fast_api_server():
        pass

    @staticmethod
    def setup(bikes):
        Bike._venv()
        Bike._env(bikes)
    
    @staticmethod
    def run():
        Bike._start_fast_api_server()
        print("Hivemind Bike server started.")

if __name__ == "__main__":
    bike = Bike()
    bike.setup()

# python -m src.setup.bike

# TODO: Arrange a Docker setup for bike repo.
