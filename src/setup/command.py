import subprocess
import sys

class Command:
    @staticmethod
    def run(command: list, cwd: str = None):
        """
        Run a shell command using subprocess.

        Args:
            command (list): The command and its arguments as a list.
            cwd (str, optional): The directory to run the command in. Defaults to None.
        """
        try:
            print(f"Running command: {' '.join(command)}")
            subprocess.check_call(command, cwd=cwd)
            print("Command executed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error: Command '{' '.join(command)}' failed with exit code {e.returncode}")
            sys.exit(1)
