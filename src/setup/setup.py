"""Module to manage the setup of the system."""

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
        """Setup the backend server."""
        Backend.run()

    @staticmethod
    def bike(start_server=True, bikes=None, already_setup=False, docker=True):
        """Setup the bike hivemind."""
        if not already_setup:
            if not bikes:
                print("No bikes provided to generate .env file for.")
            Bike.setup(bikes, docker=docker)
        if start_server:
            Bike.run()

    @staticmethod
    def frontend(start_server=True, already_setup=False):
        """Setup the frontend server."""
        if not already_setup:
            Frontend.setup()
        if start_server:
            Frontend.run()

    @staticmethod
    def master(simulation=False, rebuild=False):
        """Setup the master repository."""
        Master.setup(simulation, rebuild)
