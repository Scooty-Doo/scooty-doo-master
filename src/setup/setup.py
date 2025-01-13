from ._backend import Backend
from ._bike import Bike
from ._frontend import Frontend
from ._master import Master

class Setup:
    """
    Setup class to manage the setup of the backend, frontend, and bike instances.
    """
    @staticmethod
    def backend():
        Backend.run()

    @staticmethod
    def bike(start_server=True, bikes=None, already_setup=False, docker=True):
        if not already_setup:
            if not bikes:
                print("No bikes provided to generate .env file for.")
            Bike.setup(bikes, docker=docker)
        if start_server:
            Bike.run()

    @staticmethod
    def frontend(start_server=True, already_setup=False):
        if not already_setup:
            Frontend.setup()
        if start_server:
            Frontend.run()

    @staticmethod
    def master(simulation=False, rebuild=False):
        Master.setup(simulation, rebuild)
