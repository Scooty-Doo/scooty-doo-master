import subprocess
import sys
import os

class Command:
    @staticmethod
    def run(
        command: list,
        directory: str = None,
        asynchronous: bool = True,
        raise_exception: bool = True,
        stream_output: bool = False,
        inherit_environment: bool = False,
        **kwargs
        ):
        """
        Run a shell command using subprocess.

        Args:
            command (list): The command to run.
            directory (str, optional): The directory to run the command in. Defaults to None.
            asynchronous (bool, optional): Whether to run the command asynchronously. Defaults to True.
            raise_exception (bool, optional): Whether to raise an exception if the command fails. Defaults to True.
            stream_output (bool, optional): Whether to stream the output to the console. Defaults to False.
            inherit_environment (bool, optional): Whether to inherit the current environment variables. Defaults to False.
            **kwargs: Additional keyword arguments to pass to subprocess.
        """
        try:
            print(f"Running command: {' '.join(command)}")
            env = None
            if inherit_environment:
                #env = os.environ.copy() # TODO: Can probably be refactored away.
                env = None
            if stream_output:
                stdout = sys.stdout
                stderr = sys.stderr
            if not stream_output:
                stdout = None
                stderr = None
            if asynchronous and raise_exception:
                subprocess.check_call(command, cwd=directory, stdout=stdout, stderr=stderr, env=env, **kwargs)
            if asynchronous and not raise_exception:
                subprocess.Popen(command, cwd=directory, stdout=stdout, stderr=stderr, env=env, **kwargs)
            if not asynchronous and not raise_exception:
                subprocess.run(command, cwd=directory, check=raise_exception, stdout=stdout, stderr=stderr, env=env, **kwargs)
            if not asynchronous and raise_exception:
                subprocess.run(command, cwd=directory, check=raise_exception, stdout=stdout, stderr=stderr, env=env, **kwargs)
            print("Command executed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error: Command '{' '.join(command)}' failed with exit code {e.returncode}")
            sys.exit(1)

# TODO: What about subprocess.run() and subprocess.Popen()?