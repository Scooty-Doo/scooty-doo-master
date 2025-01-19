# pylint: disable=too-few-public-methods

import os
from ._environment import Environment
from ..utils.docker import Docker
from ..utils.directory import Directory

REPO_DIR = Directory.root()
FRONTEND_DIR = Directory.Repo.frontend()
DATABASE_CONTAINER = os.getenv("DATABASE_CONTAINER", 'database-db-1')
DATABASE_ADMINER_CONTAINER = os.getenv("DATABASE_ADMINER_CONTAINER", 'database-adminer-1')
BACKEND_CONTAINER = os.getenv("BACKEND_CONTAINER", 'api')
BIKE_CONTAINER = os.getenv("BIKE_CONTAINER", 'bike_hivemind')
SIMULATION_CONTAINER = os.getenv("SIMULATION_CONTAINER", 'simulation')
DOCKER_COMPOSE_FILENAMES = ['docker-compose.yml', 'docker-compose.simulation.yml']

class Master:
    class Docker:
        @staticmethod
        def clear(simulation=False):
            Docker.Container.delete(DATABASE_CONTAINER)
            Docker.Container.delete(DATABASE_ADMINER_CONTAINER)
            Docker.Container.delete(BACKEND_CONTAINER)
            Docker.Container.delete(BIKE_CONTAINER)
            if simulation:
                Docker.Container.delete(SIMULATION_CONTAINER)

        @staticmethod
        def build(simulation=False, rebuild=False):
            Docker.Compose.build(FRONTEND_DIR, npm=True, reinstall=rebuild)
            if not rebuild:
                return
            if not simulation:
                Docker.Compose.build(REPO_DIR)
            if simulation:
                Docker.Compose.Combined.build(REPO_DIR, filenames=DOCKER_COMPOSE_FILENAMES)

        @staticmethod
        def up(simulation=False):
            if not simulation:
                Docker.Compose.up(REPO_DIR)
            if simulation:
                Docker.Compose.Combined.up(REPO_DIR, filenames=DOCKER_COMPOSE_FILENAMES)

        @staticmethod
        def down(simulation=False):
            if not simulation:
                Docker.Compose.down(REPO_DIR)
            if simulation:
                Docker.Compose.Combined.down(REPO_DIR, filenames=DOCKER_COMPOSE_FILENAMES)

        @staticmethod
        def status(simulation):
            if not simulation:
                Docker.Compose.status(REPO_DIR)
            if simulation:
                Docker.Compose.Combined.status(REPO_DIR, filenames=DOCKER_COMPOSE_FILENAMES)

        @staticmethod
        def logs(simulation=False):
            if not simulation:
                Docker.Compose.logs(REPO_DIR)
            if simulation:
                Docker.Compose.Combined.logs(REPO_DIR, filenames=DOCKER_COMPOSE_FILENAMES)

        @staticmethod
        def restart(simulation=False, rebuild=False):
            Master.Docker.down(simulation)
            Master.Docker.clear(simulation)
            Master.Docker.build(simulation, rebuild)
            Master.Docker.up(simulation)
            Master.Docker.status(simulation)
            Master.Docker.logs(simulation)

    @staticmethod
    def setup(simulation=False, rebuild=False, start_docker_desktop=False):
        if start_docker_desktop:
            Docker.Desktop.start()
        Environment.Files.generate()
        Master.Docker.restart(simulation, rebuild)

# NOTE: Commented out as to not affect coverage.
if __name__ == "__main__": # pragma: no cover
    Master.setup()

    # python -m src.setup._master
