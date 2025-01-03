import subprocess
import sys
from ._venv import Venv
from ._environment import Environment
from ..utils.directory import Directory

ROOT_DIR = Directory.root()
REPO_DIR = Directory.Repo.frontend()
VENV_DIR = Directory.venv(REPO_DIR)
PYTHON_EXECUTABLE = Venv.get_python_executable(VENV_DIR)

class Frontend:
    """
    Frontend class to manage the setup of the frontend instance.
    """
    @staticmethod
    def _venv():
        Venv.setup(VENV_DIR)

    @staticmethod
    def _env():
        Environment.Files.generate(frontend=True)
    
    @staticmethod
    def _start_server():
        """
        Starts the frontend server.
        """
        print("Starting the frontend server...")
        #MAIN_MODULE = "placeholder"
        #try:
        #    subprocess.Popen(
        #        [PYTHON_EXECUTABLE, "-m", MAIN_MODULE],
        #        cwd=REPO_DIR,
        #        stdout=sys.stdout,
        #        stderr=sys.stderr
        #    )
        #    print("Frontend server started successfully.")
        #except Exception as e:
        #    print(f"Failed to start the frontend server: {e}")
        #    sys.exit(1)

    @staticmethod
    def setup(bikes):
        Frontend._venv()
        Frontend._env(bikes)
    
    @staticmethod
    def run():
        Frontend._start_server()
        print("Hivemind Bike server started.")

if __name__ == "__main__":
    frontend = Frontend()
    frontend.setup()

# python -m src.setup._frontend
