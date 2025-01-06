import os
import platform
import sys
from .command import Command

class Docker:
    class Compose:
        @staticmethod
        def build(directory, npm=False, reinstall=False):
            is_windows = platform.system() == "Windows"
            npm_filename = "npm.cmd" if is_windows else "npm"
            def _npm_exists():
                try:
                    Command.run([npm_filename, "--version"], inherit_environment=True)
                    return True
                except Exception:
                    return False
            if npm:
                if not _npm_exists():
                    raise Exception("NPM is not installed.")
                if (reinstall or not os.path.exists(os.path.join(directory, 'build'))):
                    try:
                        Command.run([npm_filename, "install"], directory=directory, inherit_environment=True)
                        print("Running npm install...")
                    except Exception as e:
                        print(f"Failed to run NPM install: {e}")
                        print(f"/build exists: {os.path.exists(os.path.join(directory, 'build'))}")
                        return
                try:
                    print("Running npm run build...")
                    Command.run([npm_filename, "run", "build"], directory=directory, inherit_environment=True)
                except Exception as e:
                    print(f"Failed to run NPM build: {e}")
                    return
            if not npm:
                try:
                    print("Building the Docker image...")
                    Command.run(["docker-compose", "build"], directory=directory)
                    print("Docker image built successfully.")
                except Exception as e:
                    print(f"Failed to build the Docker image: {e}")

        @staticmethod
        def up(directory, npm=False):
            Docker.Compose.down(directory)
            if not npm:
                Command.run(["docker-compose", "up", "-d"], directory=directory)
            if npm:
                Command.run(["docker-compose", "up", "webclient-prod", "-d"], directory=directory)

        @staticmethod
        def down(directory):
            Command.run(["docker-compose", "down"], directory=directory)

        @staticmethod
        def restart(directory):
            Docker.Compose.down(directory)
            Docker.Compose.up(directory)

        @staticmethod
        def status(directory):
            Command.run(["docker-compose", "ps"], directory=directory)

        @staticmethod
        def logs(directory):
            Command.run(["docker-compose", "logs", "-f"], directory=directory, raise_exception=False)
    
    class Network:
        @staticmethod
        def create(name):
            try:
                Command.run(["docker", "network", "create", name], raise_exception=True)
                print(f"Network '{name}' created successfully.")
            except Exception as e:
                print(f"Failed to create network '{name}': {e}")
        
        @staticmethod
        def recreate(name):
            if Docker.Network.exists(name):
                Docker.Network.delete(name)
            Docker.Network.create(name)

        @staticmethod
        def connect(network, container):
            try:
                Command.run(["docker", "network", "connect", network, container], raise_exception=True)
                print(f"Container '{container}' connected to network '{network}' successfully.")
            except Exception as e:
                print(f"Failed to connect container '{container}' to network '{network}': {e}")
        
        @staticmethod
        def delete(name):
            try:
                Command.run(["docker", "network", "rm", name], raise_exception=True)
                print(f"Network '{name}' deleted successfully.")
            except Exception as e:
                print(f"Failed to delete network '{name}': {e}")
        
        @staticmethod
        def disconnect(network, container):
            try:
                if not Docker.Network.is_connected(network, container):
                    print(f"Container '{container}' is not connected to network '{network}'. Skipping.")
                    return
                Command.run(["docker", "network", "disconnect", network, container], raise_exception=True)
                print(f"Container '{container}' disconnected from network '{network}' successfully.")
            except Exception as e:
                print(f"Failed to disconnect container '{container}' from network '{network}': {e}")
        
        @staticmethod
        def inspect(name):
            try:
                Command.run(["docker", "network", "inspect", name], raise_exception=True)
            except Exception as e:
                print(f"Failed to inspect network '{name}': {e}")
        
        @staticmethod
        def ls():
            try:
                Command.run(["docker", "network", "ls"], raise_exception=True)
            except Exception as e:
                print(f"Failed to display networks: {e}")
        
        @staticmethod
        def prune():
            try:
                Command.run(["docker", "network", "prune", "-f"], raise_exception=True)
                print("Pruned all unused networks successfully.")
            except Exception as e:
                print(f"Failed to prune unused networks: {e}")
        
        @staticmethod
        def exists(name):
            """
            Checks if a network exists using 'docker network ls'.
            Returns True if it exists, False otherwise.
            """
            pass
        
        @staticmethod
        def is_connected(network, container):
            pass

    class Desktop:
        @staticmethod
        def is_running():
            """
            Check if Docker Desktop is running by attempting to retrieve Docker information.
            """
            try:
                Command.run(["docker", "info"], asynchronous=False, kwargs={"verbose": False})
                print("Docker Desktop is running.")
                return True
            except Exception:
                print("Docker Desktop is not running.")
                return False

        @staticmethod
        def start():
            try:
                if Docker.Desktop.is_running():
                    print("Docker Desktop is already running.")
                    return
                print("Starting the Docker Desktop application...")
                is_windows = platform.system() == "Windows"
                if is_windows:
                    print("Starting the Docker Desktop application...")
                    docker_desktop_executable = r'C:\Program Files\Docker\Docker\Docker Desktop.exe'
                    if os.path.exists(docker_desktop_executable):
                        Command.run([docker_desktop_executable], asynchronous=False)
                else:
                    print("Please start Docker Desktop manually.")
            except Exception as e:
                print(f"Failed to start the Docker Desktop application: {e}")
                sys.exit(1)

if __name__ == "__main__":
    print(f'Docker Desktop is running: {Docker.Desktop.is_running()}')
    Docker.Desktop.start()

    # python -m src.utils.docker
