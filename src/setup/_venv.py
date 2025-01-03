import os
import platform
import subprocess
import sys
from .command import Command

IS_WINDOWS = platform.system() == "Windows"

class Venv:

    @staticmethod
    def get_python_executable(venv_dir):
        """
        Get the path to the Python executable within the virtual environment.

        Returns:
            str: Path to the Python executable.
        """
        if IS_WINDOWS:
            return os.path.join(venv_dir, "Scripts", "python.exe")
        else:
            return os.path.join(venv_dir, "bin", "python")
        
    @staticmethod
    def get_pip_executable(venv_dir):
        """
        Get the path to the pip executable within the virtual environment.

        Returns:
            str: Path to the pip executable.
        """
        if IS_WINDOWS:
            return os.path.join(venv_dir, "Scripts", "pip.exe")
        else:
            return os.path.join(venv_dir, "bin", "pip")

    @staticmethod
    def _build_venv(venv_dir):
        """
        Create a virtual environment if it doesn't exist.
        """
        if not os.path.exists(venv_dir):
            print(f"Creating virtual environment...")
            Command.run([sys.executable, "-m", "venv", venv_dir])
        else:
            print(f"Virtual environment already exists.\n")
    
    @staticmethod
    def _install_dependencies(venv_dir):
        """
        Install project dependencies using pip.
        1. Upgrade pip.
        2. Install dependencies from requirements.txt.
        """
        repo_dir = os.path.dirname(venv_dir) # Get the directory of the virtual environment
        python_executable = Venv.get_python_executable(venv_dir)

        print(f"Installing dependencies...")
        try:
            Command.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
            requirements_path = os.path.join(repo_dir, "requirements.txt")
            Command.run([python_executable, "-m", "pip", "install", "-r", requirements_path], cwd=repo_dir)
            print(f"Dependencies installed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Dependency installation failed: {e}")
            sys.exit(1)

    def setup(venv_dir):
        Venv._build_venv(venv_dir)
        Venv._install_dependencies(venv_dir)
