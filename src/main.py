import os
import logging
from dotenv import load_dotenv

load_dotenv()

from .setup.setup import Setup
from .data.get import Get
from .utils.settings import Settings
from .utils.repositories import Repositories
from .utils.chrome import Chrome
from .utils.directory import Directory

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

    def _setup_master(self):
        Setup.master()

    def _open_chrome_tabs(self, bikes=True, frontend=True): # NOTE: Maybe remove due to OS dependency?
        ports = [os.getenv("BACKEND_PORT") + "/docs"]
        if bikes:
            ports.append(os.getenv("BIKES_PORT") + "/docs")
        if frontend:
            ports.append(os.getenv("FRONTEND_PORT"))
        Chrome.Open.window(*ports)

    def run(self, open_chrome_tabs=True):
        self._setup_master()
        if open_chrome_tabs:
            self._open_chrome_tabs(bikes=True, frontend=True)

if __name__ == "__main__":

    # NOTE: Run to auto-setup venv in master repository:
    # python -m src.setup._venv

    main = Main(
        use_submodules=False
    )
    main.run(
        open_chrome_tabs=True
    )

# python -m src.main


# python -m pytest --cov=src --cov-report=html 
# python -m pytest --cov=src --cov-report=term-missing

# TODO: Bash script to run the program?
