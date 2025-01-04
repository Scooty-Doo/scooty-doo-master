import subprocess
import sys

class Command:
    @staticmethod
    def run(
        command: list,
        directory: str = None,
        asynchronous: bool = True,
        raise_exception: bool = True,
        stream_output: bool = False,
        # TODO: Maybe add a log_file parameter to log the output to a file.
        ):
        """
        Run a shell command using subprocess.

        Args:
            command (list): The command and its arguments as a list.
            cwd (str, optional): The directory to run the command in. Defaults to None.
        """
        try:
            print(f"Running command: {' '.join(command)}")
            if stream_output:
                stdout = sys.stdout
                stderr = sys.stderr
            if not stream_output:
                stdout = None
                stderr = None
            if asynchronous and raise_exception:
                subprocess.check_call(command, cwd=directory, stdout=stdout, stderr=stderr)
            if asynchronous and not raise_exception:
                subprocess.Popen(command, cwd=directory, stdout=stdout, stderr=stderr)
            if not asynchronous and not raise_exception:
                subprocess.run(command, cwd=directory, check=raise_exception, stdout=stdout, stderr=stderr)
            if not asynchronous and raise_exception:
                subprocess.run(command, cwd=directory, check=raise_exception, stdout=stdout, stderr=stderr)
            print("Command executed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error: Command '{' '.join(command)}' failed with exit code {e.returncode}")
            sys.exit(1)

# TODO: What about subprocess.run() and subprocess.Popen()?