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
        def _clear():
            Docker.Container.delete(DATABASE_CONTAINER)
            Docker.Container.delete(DATABASE_ADMINER_CONTAINER)
            Docker.Container.delete(BACKEND_CONTAINER)

    @staticmethod
    def _setup():
        Backend.Docker._down()
        Backend.Docker._clear()
        Backend.Docker._build()
        Backend.Docker._up()
        Backend.Docker.status()
        Backend.Docker.logs()

    @staticmethod
    def run():
        Backend._setup()

if __name__ == "__main__":
    backend = Backend()
    backend.run()
    #backend.Docker._down()
    #backend.Docker._clear()

    # Optional: Uncomment the following line to run tests after setting up the backend
    #backend.run_tests()

# python -m src.setup._backend
# NOTE: You need to start Docker Desktop for it to work.
# TODO: Start Docker Desktop automatically with subprocess if not running?
# NOTE: .env in repos/backend/.env need to be setup with the correct values (see env/examples folder).
