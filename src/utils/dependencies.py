import os
from ..utils.command import Command

class Dependencies:
    class Pip:
        @staticmethod
        def upgrade(python_executable):
            Command.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"])

    @staticmethod
    def install(python_executable, repo_dir, upgrade_pip=True):
        requirements_path = os.path.join(repo_dir, "requirements.txt")
        if upgrade_pip:
            Dependencies.Pip.upgrade(python_executable)
        Command.run([python_executable, "-m", "pip", "install", "-r", requirements_path], directory=repo_dir)