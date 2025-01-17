"""Module to manage the setup of the virtual environment."""

import os
import platform
import subprocess
import sys
from ..utils.command import Command
from ..utils.dependencies import Dependencies
from ..utils.directory import Directory

IS_WINDOWS = platform.system() == "Windows"

class Venv:
    """Class to manage the setup of the virtual environment."""
    @staticmethod
    def get_python_executable(venv_dir):
        """
        Get the path to the Python executable within the virtual environment.
        """
        if IS_WINDOWS:
            return os.path.join(venv_dir, "Scripts", "python.exe")
        return os.path.join(venv_dir, "bin", "python")

    @staticmethod
    def _build_venv(venv_dir):
        """
        Create a virtual environment if it doesn't exist.
        """
        if not os.path.exists(venv_dir):
            print("Creating virtual environment...")
            Command.run([sys.executable, "-m", "venv", venv_dir])
        else:
            print("Virtual environment already exists.\n")

    @staticmethod
    def _install_dependencies(venv_dir):
        """
        Install project dependencies using pip.
        1. Upgrade pip.
        2. Install dependencies from requirements.txt.
        """
        repo_dir = os.path.dirname(venv_dir) # Get the directory of the virtual environment
        python_executable = Venv.get_python_executable(venv_dir)

        print("Installing dependencies...")
        try:
            Dependencies.install(python_executable, repo_dir)
            print("Dependencies installed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Dependency installation failed: {e}")
            sys.exit(1)

    @staticmethod
    def setup(venv_dir):
        """Setup the virtual environment."""
        Venv._build_venv(venv_dir)
        Venv._install_dependencies(venv_dir)

    @staticmethod
    def setup_master():
        """
        Setup the master virtual environment.
        """
        venv_dir = os.path.join(Directory.root(), "venv")
        Venv.setup(venv_dir)

# NOTE: Commented out as to not affect test coverage.
# if __name__ == "__main__":
#     Venv.setup_master()

    # python -m src.setup._venv
