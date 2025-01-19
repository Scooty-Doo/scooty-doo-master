# pylint: disable=too-few-public-methods
"""Module to manage the dependencies of the project."""

import os
from ..utils.command import Command

class Dependencies:
    """Class to manage the dependencies of the project."""
    class Pip:
        """Class to manage the pip dependencies of the project."""
        @staticmethod
        def upgrade(python_executable):
            """Upgrade pip to the latest version."""
            Command.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"])

    @staticmethod
    def install(python_executable, repo_dir, upgrade_pip=True):
        """Install the dependencies of the project."""
        requirements_path = os.path.join(repo_dir, "requirements.txt")
        if upgrade_pip:
            Dependencies.Pip.upgrade(python_executable)
        Command.run(
            [python_executable, "-m", "pip", "install", "-r",
             requirements_path], directory=repo_dir)
