from ..utils.directory import Directory
from ..utils.command import Command

BACKEND_DIR = Directory.Repo.backend()
BIKE_DIR = Directory.Repo.bike()
FRONTEND_DIR = Directory.Repo.frontend()

class Master:
    @staticmethod
    def _delete_venv():
        for directory in [BACKEND_DIR, BIKE_DIR, FRONTEND_DIR]:
            Command.run(["rm", "-rf", Directory.venv(directory)])
        

    @staticmethod
    def setup():
        Master._delete_venv()

if __name__ == "__main__":
    Master.setup()

    # python -m src.setup._master