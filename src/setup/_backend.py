import sys
import time
from ._venv import Venv
from ..utils.command import Command
from ..utils.docker import Docker
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
    class Docker:
        @staticmethod
        def _build():
            try:
                print("Building the backend Docker image...")
                Docker.Compose.build(REPO_DIR)
            except Exception as e:
                print(f"Failed to build the backend Docker image: {e}")
                sys.exit(1)

        @staticmethod
        def _up():
            try:
                print("Starting the backend Docker container...")
                Docker.Compose.up(REPO_DIR)
            except Exception as e:
                print(f"Failed to start the backend Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _down():
            try:
                print("Stopping the backend Docker container...")
                Docker.Compose.down(REPO_DIR)
            except Exception as e:
                print(f"Failed to stop the backend Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _restart():
            Backend.Docker._down()
            Backend.Docker._up()

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
    def _database():
        try:
            Docker.Desktop.start()
            print("Starting PostgreSQL and pgAdmin containers...")
            Docker.Compose.up(DATABASE_DIR)
            print("Creating database tables...")
            table_creation_module = "api.db.table_creation"
            Command.run([PYTHON_EXECUTABLE, "-m", table_creation_module], directory=REPO_DIR)
        except Exception as e:
            print(f"Make sure Docker Desktop is running. Failed to setup the database: {e}")

    @staticmethod
    def _mock_data():
        print("Loading mock data into the database...")
        load_mock_data_module = "database.load_mock_data"
        Command.run([PYTHON_EXECUTABLE, "-m", load_mock_data_module], directory=REPO_DIR)

    @staticmethod
    def _start_server(docker=True):
        if docker:
            Backend.Docker._up()
            Backend.Docker.status()
            Backend.Docker.logs()
            return
        print("Starting the FastAPI server...")
        command = [
            PYTHON_EXECUTABLE,
            "-m",
            "uvicorn",
            "api.main:app",
            "--reload",
        ]
        try:
            Command.run(command, REPO_DIR, asynchronous=True, raise_exception=False, stream_output=False)
        except Exception as e:
            print(f"Failed to start the FastAPI server: {e}")
            sys.exit(1)

    @staticmethod
    def setup(docker=True):
        Backend._venv()
        Backend._database()
        time.sleep(5)
        Backend._mock_data()
        if docker:
            Backend.Docker._build()

    @staticmethod
    def run(docker=True):
        Backend._start_server(docker)
        time.sleep(5)

    @staticmethod
    def tests():
        """
        Run tests using pytest with optional coverage.
        """
        print("Running tests without coverage...")
        Command.run([PYTHON_EXECUTABLE, "-m", "pytest"], directory=REPO_DIR)
        print("Running tests with coverage...")
        Command.run([PYTHON_EXECUTABLE, "-m", "coverage", "run", "-m", "pytest"], directory=REPO_DIR)
        print("Generating coverage report...")
        Command.run([PYTHON_EXECUTABLE, "-m", "coverage", "report"], directory=REPO_DIR)
        print("Generating HTML coverage report...")
        Command.run([PYTHON_EXECUTABLE, "-m", "coverage", "html"], directory=REPO_DIR)
        print("Coverage reports generated.\n")

if __name__ == "__main__":
    backend = Backend()
    backend.run()

    # Optional: Uncomment the following line to run tests after setting up the backend
    #backend.run_tests()

# python -m src.setup._backend
# NOTE: You need to start Docker Desktop for it to work.
# TODO: Start Docker Desktop automatically with subprocess if not running?
# NOTE: .env in repos/backend/.env need to be setup with the correct values (see env/examples folder).
