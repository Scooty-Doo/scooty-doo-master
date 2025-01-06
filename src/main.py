import os
from dotenv import load_dotenv

load_dotenv()

from .setup.setup import Setup
from .data.get import Get
from .utils.settings import Settings
from .utils.repositories import Repositories
from .utils.chrome import Chrome
from .utils.docker import Docker

class Main:
    def __init__(self, use_submodules=False):
        self.get = Get()
        self.repositories = Repositories()
        if use_submodules:
            self._use_submodules()
        if not use_submodules:
            self._use_local_repositories()

    def _use_submodules(self, auto_pull=True):
        """Changes the REPOSITORIES_DIRECTORY environment variable to the submodules directory."""
        os.environ["REPOSITORIES_DIRECTORY"] = Settings.Directory.Name.submodules
        if auto_pull:
            self.repositories.submodules.get.all()

    def _use_local_repositories(self):
        """Pull repositories to the local repositories folder."""
        os.environ["REPOSITORIES_DIRECTORY"] = Settings.Directory.local_repositories
        self.repositories.local.get.all(branch='main')

    def _setup_backend(self, start_server, already_setup, docker=True):
        Setup.backend(start_server, already_setup, docker)

    def _setup_bikes(self, start_server, already_setup, docker=True, master_docker_compose_file=True):
        bikes = None
        if not already_setup:
            bikes = self.get.bikes()
        Setup.bike(start_server, bikes, already_setup, docker, master_docker_compose_file=master_docker_compose_file)

    def _setup_frontend(self):
        Setup.frontend()

    #def get_all(self):
    #    self.bikes = self.get.bikes()
    #    self.trips = self.get.trips()
    #    self.users = self.get.users()
    #    self.zones = self.get.zones()
    #    self.zone_types = self.get.zone_types()

    def _open_chrome_tabs(self, bikes=True, frontend=True):
        ports = [os.getenv("BACKEND_PORT") + "/docs"]
        if bikes:
            ports.append(os.getenv("BIKES_PORT") + "/docs")
        if frontend:
            ports.append(os.getenv("FRONTEND_PORT"))
        Chrome.Open.window(*ports)

    def run(self, skip_setup=False, bikes=True, frontend=False, open_chrome_tabs=False, docker=True, master_docker_compose_file=True):
        if docker and not master_docker_compose_file:
            print("Checking if network exists...")
            Docker.Network.disconnect(network="scooty-web", container="api")
            Docker.Network.disconnect(network="scooty-web", container="bike_hivemind_app")
            Docker.Network.recreate(name="scooty-web")
        self._setup_backend(start_server=True, already_setup=skip_setup, docker=docker)
        if docker and not master_docker_compose_file:
            Docker.Network.connect(network="scooty-web", container="api")
        if bikes:
            self._setup_bikes(start_server=True, already_setup=skip_setup, docker=docker, master_docker_compose_file=master_docker_compose_file)
            if docker and not master_docker_compose_file:
                Docker.Network.connect(network="scooty-web", container="bike_hivemind_app")
        if frontend:
            self._setup_frontend(start_server=True, already_setup=skip_setup)
        if open_chrome_tabs:
            self._open_chrome_tabs(bikes=bikes, frontend=frontend)

if __name__ == "__main__":

    # NOTE: Run to auto-setup venv in master repository:
    # python -m src.setup._venv

    main = Main(
        use_submodules=False
    )
    main.run(
        skip_setup=False,
        bikes=True,
        frontend=False,
        open_chrome_tabs=True,
        docker=True,
        master_docker_compose_file=False
    )

# python -m src.main


# python -m pytest --cov=src --cov-report=html 
# python -m pytest --cov=src --cov-report=term-missing

# TODO: Bash script to run the program?
