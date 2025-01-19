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
        return_output: bool = False,
        inherit_environment: bool = False,
        **kwargs
        ):
        """
        Run a shell command using subprocess.

        Args:
            command (list):
                The command to run.
            directory (str, optional):
                The directory to run the command in.
            asynchronous (bool, optional):
                Whether to run the command asynchronously.
            raise_exception (bool, optional):
                Whether to raise an exception if the command fails.
            stream_output (bool, optional): 
                Whether to stream the output to the console.
            inherit_environment (bool, optional):
                Whether to inherit the current environment variables.
            **kwargs:
                Additional keyword arguments to pass to subprocess.
        """
        try:
            print(f"Running command: {' '.join(command)}")
            env = None
            if inherit_environment:
                #env = os.environ.copy() # NOTE: Can probably be refactored away.
                env = None
            stdout = None
            stderr = None
            if stream_output:
                stdout = sys.stdout
                stderr = sys.stderr
            if return_output:
                stdout = subprocess.PIPE
                stderr = subprocess.PIPE

            if asynchronous and raise_exception:
                subprocess.check_call(
                    command, cwd=directory, stdout=stdout, stderr=stderr, env=env, **kwargs)
            if asynchronous and not raise_exception:
                subprocess.Popen( # pylint: disable=consider-using-with
                    command, cwd=directory, stdout=stdout, stderr=stderr, env=env, **kwargs)
            if not asynchronous and not raise_exception:
                subprocess.run(
                    command, cwd=directory, check=raise_exception, stdout=stdout,
                    stderr=stderr, env=env, **kwargs)
            if not asynchronous and raise_exception:
                subprocess.run(
                    command, cwd=directory, check=raise_exception, stdout=stdout,
                    stderr=stderr, env=env, **kwargs)
            print("Command executed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"Error: Command '{' '.join(command)}' failed with exit code {e.returncode}")
            if raise_exception:
                sys.exit(1)
