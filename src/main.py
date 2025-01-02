from dotenv import load_dotenv
load_dotenv()
from .setup.setup import Setup
from .data.get import Get

class Main:
    def __init__(self):
        self.get = Get()

    def _setup_backend(self, start_server, already_setup):
        Setup.backend(start_server, already_setup)

    def _setup_bikes(self, start_server, already_setup):
        bikes = None
        if not already_setup:
            bikes = self.get.bikes()
        Setup.bike(start_server, bikes, already_setup)

    def _setup_frontend(self):
        Setup.frontend()

    #def get_all(self):
    #    self.bikes = self.get.bikes()
    #    self.trips = self.get.trips()
    #    self.users = self.get.users()
    #    self.zones = self.get.zones()
    #    self.zone_types = self.get.zone_types()
    
    def run(self, skip_setup=False, bikes=True, frontend=False):
        self._setup_backend(start_server=True, already_setup=skip_setup)
        if bikes:
            self._setup_bikes(start_server=True, already_setup=skip_setup)
        if frontend:
            self._setup_frontend()

if __name__ == "__main__":
    main = Main()
    main.run(
        skip_to_start_server=True,
        bikes=True,
        frontend=False
    )

# TODO: Next step is to init the Hivemind (repos/bike/src/main.py) server.
#       Put the logic in src.setup.bike.py > Bike._start_fast_api_server().

# NOTE: Run "python -m get_repos" to fetch the repos (backend, frontend, bike) to /repos.
# python -m src.main
