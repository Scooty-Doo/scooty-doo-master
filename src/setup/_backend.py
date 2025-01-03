import subprocess
import sys
import time
from ._venv import Venv
from .command import Command
from ..utils.directory import Directory

ROOT_DIR = Directory.root()
REPO_DIR = Directory.Repo.backend()
DATABASE_DIR = Directory.database()
VENV_DIR = Directory.venv(REPO_DIR)
PYTHON_EXECUTABLE = Venv.get_python_executable(VENV_DIR)

class Backend:
    """
    Backend class to manage the setup of the backend server.
    """
    @staticmethod
    def _setup_venv():
        Venv.setup(VENV_DIR)

    @staticmethod
    def _setup_database():
        try:
            print("Starting PostgreSQL and pgAdmin containers...")
            Command.run(["docker-compose", "up", "-d"], cwd=DATABASE_DIR)
            print("Creating database tables...")
            table_creation_module = "api.db.table_creation"
            Command.run([PYTHON_EXECUTABLE, "-m", table_creation_module], cwd=REPO_DIR)
        except Exception as e:
            print(f"Make sure Docker Desktop is running. Failed to setup the database: {e}")

    @staticmethod
    def _load_mock_data():
        print("Loading mock data into the database...")
        load_mock_data_module = "database.load_mock_data"
        Command.run([PYTHON_EXECUTABLE, "-m", load_mock_data_module], cwd=REPO_DIR)

    @staticmethod
    def _start_api_server():
        print("Starting the FastAPI server...")
        uvicorn_command = [
            PYTHON_EXECUTABLE,
            "-m",
            "uvicorn",
            "api.main:app",
            "--reload",
        ]
        try:
            subprocess.Popen(uvicorn_command, cwd=REPO_DIR)
        except Exception as e:
            print(f"Failed to start the FastAPI server: {e}")
            sys.exit(1)
    
    @staticmethod
    def setup():
        Backend._setup_venv()
        Backend._setup_database()
        time.sleep(5)
        Backend._load_mock_data()

    @staticmethod
    def run():
        Backend._start_api_server()

    @staticmethod
    def run_tests(self):
        """
        Run tests using pytest with optional coverage.
        """
        print("Running tests without coverage...")
        Command.run([PYTHON_EXECUTABLE, "-m", "pytest"], cwd=REPO_DIR)
        print("Running tests with coverage...")
        Command.run([PYTHON_EXECUTABLE, "-m", "coverage", "run", "-m", "pytest"], cwd=REPO_DIR)
        print("Generating coverage report...")
        Command.run([PYTHON_EXECUTABLE, "-m", "coverage", "report"], cwd=REPO_DIR)
        print("Generating HTML coverage report...")
        Command.run([PYTHON_EXECUTABLE, "-m", "coverage", "html"], cwd=REPO_DIR)
        print("Coverage reports generated.\n")

if __name__ == "__main__":
    """
    Entry point for the script.
    Usage:
        python src/backend.py
    """
    backend = Backend()
    backend.run()

    # Optional: Uncomment the following line to run tests after setting up the backend
    #backend.run_tests()

# python -m src.setup.backend
# NOTE: You need to start Docker Desktop for it to work.
# TODO: Start Docker Desktop automatically with subprocess if not running?
# NOTE: .env in repos/backend/.env need to be setup with the correct values (see env/examples folder).
