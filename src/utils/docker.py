# pylint: disable=broad-exception-raised, broad-exception-caught, too-few-public-methods

import os
import platform
import sys
import time
import shutil
import yaml
from .command import Command
from .directory import Directory

ROOT_DIR = Directory.root()
DOCKER_COMPOSE_FILENAME = "docker-compose.yml"
DOCKER_COMPOSE_RESET_FILENAME = "docker-compose.reset.yml"
DOCKER_COMPOSE_SIMULATION_FILENAME = "docker-compose.simulation.yml"

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
                        Command.run(
                            [npm_filename, "install"],
                            directory=directory,
                            inherit_environment=True
                            )
                        print("Running npm install...")
                    except Exception as e:
                        print(f"Failed to run NPM install: {e}")
                        print(f"/build exists: {os.path.exists(os.path.join(directory, 'build'))}")
                        return
                try:
                    print("Running npm run build...")
                    Command.run(
                        [npm_filename, "run", "build"],
                        directory=directory,
                        inherit_environment=True
                        )
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
                Command.run(
                    ["docker-compose", "up", "-d", "--build"],
                    directory=directory
                    )
            if npm:
                Command.run(
                    ["docker-compose", "up", "webclient-prod", "-d"],
                    directory=directory
                    )

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
            Command.run(
                ["docker-compose", "logs", "-f"],
                directory=directory,
                raise_exception=False
                )

        class Combined:
            @staticmethod
            def _combine_into_command(filenames, command):
                """
                Combines docker-compose files into a single command.
                """
                compose_files = []
                for filename in filenames:
                    compose_files.extend(["-f", filename])
                return ["docker-compose"] + compose_files + command

            @staticmethod
            def build(directory, filenames):
                Command.run(Docker.Compose.Combined._combine_into_command(
                    filenames, ["build"]), directory=directory, raise_exception=False)

            @staticmethod
            def up(directory, filenames):
                Command.run(Docker.Compose.Combined._combine_into_command(
                    filenames, ["up", "-d"]), directory=directory, raise_exception=False)

            @staticmethod
            def down(directory, filenames):
                Command.run(Docker.Compose.Combined._combine_into_command(
                    filenames, ["down"]), directory=directory, raise_exception=False)

            @staticmethod
            def status(directory, filenames):
                Command.run(Docker.Compose.Combined._combine_into_command(
                    filenames, ["ps"]), directory=directory, raise_exception=False)

            @staticmethod
            def logs(directory, filenames):
                Command.run(Docker.Compose.Combined._combine_into_command(
                    filenames, ["logs", "-f"]), directory=directory, raise_exception=False)

        class Environment:
            @staticmethod
            def set(service, variable, value):
                if service == "simulation":
                    docker_compose_file = os.path.join(ROOT_DIR, DOCKER_COMPOSE_SIMULATION_FILENAME)
                else:
                    docker_compose_file = os.path.join(ROOT_DIR, DOCKER_COMPOSE_FILENAME)
                backup_file = docker_compose_file + ".backup"
                if not os.path.exists(docker_compose_file):
                    raise FileNotFoundError(f"{docker_compose_file} does not exist.")
                shutil.copyfile(docker_compose_file, backup_file)
                print(f"Backup created at {backup_file}.")
                with open(docker_compose_file, 'r', encoding='utf-8') as file:
                    docker_compose = yaml.safe_load(file)
                services = docker_compose.get('services', {})
                if service not in services:
                    raise ValueError(f"Service '{service}' not found.")
                service = services[service]
                environment = service.get('environment', {})
                if environment is None or isinstance(environment, list):
                    raise TypeError(
                        f"Environment for service '{service}' must be a key-value dictionary.")
                environment[variable] = value
                service['environment'] = environment
                with open(docker_compose_file, 'w', encoding='utf-8') as file:
                    yaml.safe_dump(docker_compose, file, default_flow_style=False)
                print(
                    f"Updated '{variable}' for service '{service}' to \
                        '{value}' in {docker_compose_file}.")

            @staticmethod
            def reset(simulation=False):
                if not simulation:
                    docker_compose_file = os.path.join(ROOT_DIR, DOCKER_COMPOSE_FILENAME)
                    reset_file = os.path.join(ROOT_DIR, DOCKER_COMPOSE_RESET_FILENAME)
                    if not os.path.exists(reset_file):
                        raise FileNotFoundError(f"{reset_file} does not exist.")
                    shutil.copyfile(reset_file, docker_compose_file)
                    print(f"Reset Docker Compose file to {reset_file}.")
                if simulation:
                    docker_compose_file = os.path.join(ROOT_DIR, DOCKER_COMPOSE_SIMULATION_FILENAME)
                    reset_file = os.path.join(ROOT_DIR, DOCKER_COMPOSE_RESET_FILENAME)
                    if not os.path.exists(reset_file):
                        raise FileNotFoundError(f"{reset_file} does not exist.")
                    shutil.copyfile(reset_file, docker_compose_file)
                    print(f"Reset Docker Compose file to {reset_file}.")

    class Container:
        @staticmethod
        def stop(name):
            try:
                Command.run(
                    ["docker", "stop", name],
                    asynchronous=False,
                    raise_exception=False
                    )
                print(f"Container '{name}' stopped successfully.")
            except Exception as e:
                print(f"Failed to stop container '{name}': {e}")

        @staticmethod
        def delete(name):
            try:
                Command.run(
                    ["docker", "rm", "-f", name],
                    asynchronous=False,
                    raise_exception=False
                    )
                print(f"Container '{name}' deleted successfully.")
            except Exception as e:
                print(f"Failed to delete container '{name}': {e}")

    class Network:
        @staticmethod
        def create(name):
            try:
                Command.run(
                    ["docker", "network", "create", name],
                    asynchronous=False, raise_exception=False)
                print(f"Network '{name}' created successfully.")
            except Exception as e:
                print(f"Failed to create network '{name}': {e}")

        @staticmethod
        def recreate(name):
            Docker.Network.delete(name)
            Docker.Network.create(name)

        @staticmethod
        def connect(network, container):
            try:
                Command.run(
                    ["docker", "network", "connect", network, container],
                    asynchronous=False,
                    raise_exception=False
                    )
                print(f"Container '{container}' connected to network '{network}' successfully.")
            except Exception as e:
                print(f"Failed to connect container '{container}' to network '{network}': {e}")

        @staticmethod
        def delete(name):
            try:
                Command.run(
                    ["docker", "network", "rm", name],
                    asynchronous=False,
                    raise_exception=False
                    )
                print(f"Network '{name}' deleted successfully.")
            except Exception as e:
                print(f"Failed to delete network '{name}': {e}")

        @staticmethod
        def disconnect(network, container):
            try:
                Command.run(
                    ["docker", "network", "disconnect", network, container],
                    asynchronous=False,
                    raise_exception=False
                    )
                print(
                    f"Container '{container}' disconnected from network '{network}' successfully.")
            except Exception as e:
                print(
                    f"Failed to disconnect container '{container}' from network '{network}': {e}")

        @staticmethod
        def inspect(name):
            try:
                Command.run(
                    ["docker", "network", "inspect", name],
                    asynchronous=False,
                    raise_exception=False
                    )
            except Exception as e:
                print(f"Failed to inspect network '{name}': {e}")

        @staticmethod
        def show():
            try:
                Command.run(
                    ["docker", "network", "ls"],
                    asynchronous=False,
                    raise_exception=False
                    )
            except Exception as e:
                print(f"Failed to display networks: {e}")

        @staticmethod
        def prune():
            try:
                Command.run(
                    ["docker", "network", "prune", "-f"],
                    asynchronous=False,
                    raise_exception=False
                    )
                print("Pruned all unused networks successfully.")
            except Exception as e:
                print(f"Failed to prune unused networks: {e}")

    class Desktop:
        @staticmethod
        def is_running():
            """
            Check if Docker Desktop is running by attempting to retrieve Docker information.
            """
            try:
                Command.run(
                    ["docker", "info"],
                    asynchronous=False,
                    kwargs={"verbose": False}
                    )
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
                        time.sleep(10)
                else:
                    print("Please start Docker Desktop manually.")
            except Exception as e:
                print(f"Failed to start the Docker Desktop application: {e}")
                sys.exit(1)

if __name__ == "__main__": # pragma: no cover
    #print(f'Docker Desktop is running: {Docker.Desktop.is_running()}')
    #Docker.Desktop.start()

    Docker.Compose.Environment.set("bike_hivemind", "DEFAULT_SPEED", 1000)

    # python -m src.utils.docker
