from .setup._venv import Venv
Venv.setup_master()
import os
import logging
import platform
from dotenv import load_dotenv

load_dotenv()

from .setup.setup import Setup
from .data.get import Get
from .utils.settings import Settings
from .utils.repositories import Repositories
from .utils.chrome import Chrome
from .utils.directory import Directory
from .utils.docker import Docker

BIKE_SERVICE_NAME = os.getenv("BIKE_CONTAINER")
SIMULATION_SERVICE_NAME = os.getenv("SIMULATION_CONTAINER")

LOGS_DIR = Directory.logs()
os.makedirs(LOGS_DIR, exist_ok=True)

def setup_logger():
    logger = logging.getLogger('master')
    logger.setLevel(logging.DEBUG)
    log_file = os.path.join(LOGS_DIR, 'master.log')
    fh = logging.FileHandler(log_file)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

logger = setup_logger()

class Main:
    def __init__(self, use_submodules=False,
                 backend_branch='main', backend_commit=None,
                 frontend_branch='main', frontend_commit=None,
                 bike_branch='main', bike_commit=None):
        self.get = Get()
        self.repositories = Repositories()
        self.backend_branch = backend_branch
        self.backend_commit = backend_commit
        self.frontend_branch = frontend_branch
        self.frontend_commit = frontend_commit
        self.bike_branch = bike_branch
        self.bike_commit = bike_commit
        if use_submodules:
            self._use_submodules()
        if not use_submodules:
            self._use_local_repositories()
        logger.info("Main initialized.")
        logger.debug(f"REPOSITORIES_DIRECTORY: {os.getenv('REPOSITORIES_DIRECTORY')}")

    def _use_submodules(self, auto_pull=True):
        """Changes the REPOSITORIES_DIRECTORY environment variable to the submodules directory."""
        os.environ["REPOSITORIES_DIRECTORY"] = Settings.Directory.Name.submodules
        if auto_pull:
            self.repositories.submodules.get.all()

    def _use_local_repositories(self):
        """Pull repositories to the local repositories folder."""
        os.environ["REPOSITORIES_DIRECTORY"] = Settings.Directory.local_repositories
        self.repositories.local.get.backend(branch=self.backend_branch, commit=self.backend_commit)
        self.repositories.local.get.frontend(branch=self.frontend_branch, commit=self.frontend_commit)
        self.repositories.local.get.bike(branch=self.bike_branch, commit=self.bike_commit)

    def _setup_master(self, simulation=False, rebuild=False):
        Setup.master(simulation, rebuild)

    def _open_chrome_tabs(self, bikes=True, frontend=True): # NOTE: Maybe remove due to OS dependency?
        if not platform.system() == "Windows":
            return
        ports = [os.getenv("BACKEND_PORT") + "/docs"]
        if bikes:
            ports.append(os.getenv("BIKES_PORT") + "/docs")
        if frontend:
            ports.append(os.getenv("FRONTEND_PORT"))
        Chrome.Open.window(*ports)

    def _run(self, simulation=True, simulation_speed_factor=1.0, rebuild=False, open_chrome_tabs=False, bike_limit=9999):
        if simulation_speed_factor == 1.0 or (bike_limit == 9999 or bike_limit is None):
            Docker.Compose.Environment.reset(simulation=False)
        if bike_limit == 9999 or bike_limit is None:
            Docker.Compose.Environment.reset(simulation=True)
        if simulation_speed_factor != 1.0:
            default_speed_kmh = 20.0
            simulation_speed_kmh = default_speed_kmh * simulation_speed_factor
            Docker.Compose.Environment.set(BIKE_SERVICE_NAME, "DEFAULT_SPEED", int(simulation_speed_kmh))
        if bike_limit != 9999 and bike_limit is not None:
            Docker.Compose.Environment.set(BIKE_SERVICE_NAME, "BIKE_LIMIT", bike_limit)
            Docker.Compose.Environment.set(SIMULATION_SERVICE_NAME, "BIKE_LIMIT", bike_limit)

        self._setup_master(simulation, rebuild)

        if open_chrome_tabs:
            self._open_chrome_tabs(bikes=True, frontend=True)

    def run(self, simulation_speed_factor=1.0, open_chrome_tabs=True, rebuild=False, bike_limit=9999):
        self._run(simulation=False, simulation_speed_factor=simulation_speed_factor, rebuild=rebuild, open_chrome_tabs=open_chrome_tabs, bike_limit=bike_limit)

    def simulate(self, simulation_speed_factor=1.0, open_chrome_tabs=True, rebuild=False, bike_limit=9999):
        self._run(simulation=True, simulation_speed_factor=simulation_speed_factor, rebuild=rebuild, open_chrome_tabs=open_chrome_tabs, bike_limit=bike_limit)

if __name__ == "__main__":

# NOTE: Master setup happens automatically every time (see top of this module).
#    SETUP_MASTER_VENV = True
#
#    from .setup._venv import Venv
#    if SETUP_MASTER_VENV:
#        Venv.setup_master()

    main = Main(
        use_submodules=False,
        backend_branch='main',
        backend_commit=None,
        frontend_branch='main',
        frontend_commit=None,
        bike_branch='main',
        bike_commit=None
    )

    options = {
        "simulation_speed_factor": 1000.0,
        "bike_limit": 100, # 9999 or None for no limit
        "rebuild": True,
        "open_chrome_tabs": False
        }

    SIMULATION = True

    if SIMULATION:
        main.simulate(**options)
    if not SIMULATION:
        main.run(**options)

# python -m src.main


# python -m pytest --cov=src --cov-report=html
# python -m pytest --cov=src --cov-report=term-missing

# TODO: Bash script to run the program?
