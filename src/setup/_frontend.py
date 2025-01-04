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
        Environment.Files.generate(frontend=True)

    class Docker:
        @staticmethod
        def _build():
            print("Building the frontend Docker image...")
            try:
                Docker.Compose.build(REPO_DIR, npm=True, reinstall=True)
                print("Frontend Docker image built successfully.")
            except Exception as e:
                print(f"Failed to build the frontend Docker image: {e}")
                sys.exit(1)

        @staticmethod
        def _start():
            print("Starting the frontend Docker container...")
            try:
                Docker.Compose.up(REPO_DIR)
                print("Frontend Docker container started successfully.")
            except Exception as e:
                print(f"Failed to start the frontend Docker container: {e}")
                sys.exit(1)

        @staticmethod
        def _stop():
            print("Stopping the frontend Docker container...")
            try:
                Docker.Compose.down(REPO_DIR)
                print("Frontend Docker container stopped successfully.")
            except Exception as e:
                print(f"Failed to stop the frontend Docker container: {e}")
                sys.exit(1)
        
        @staticmethod
        def _restart():
            Frontend.Docker._stop()
            Frontend.Docker._start()

        @staticmethod
        def status():
            Docker.Compose.status(REPO_DIR)

    @staticmethod
    def setup():
        Frontend._env()
        Frontend.Docker._build()
    
    @staticmethod
    def run():
        Frontend.Docker._restart()
        Frontend.Docker.status()
        print("Hivemind Bike server started.")

if __name__ == "__main__":
    frontend = Frontend()
    frontend.setup()
    frontend.run()
    frontend.Docker.status()

# python -m src.setup._frontend
