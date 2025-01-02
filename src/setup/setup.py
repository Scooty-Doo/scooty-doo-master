from ._backend import Backend
from ._bike import Bike
from ._frontend import Frontend

class Setup:
    """
    Setup class to manage the setup of the backend, frontend, and bike instances.
    """
    @staticmethod
    def backend(start_server=True, already_setup=True):
        if not already_setup:
            Backend.setup()
        if start_server:    
            Backend.run()

    @staticmethod
    def bike(start_server=True, bikes=None, already_setup=False):
        if not already_setup:
            if not bikes:
                print("No bikes provided to generate .env file for.")
            Bike.setup(bikes)
        if start_server:
            Bike.run()
    
    @staticmethod
    def frontend():
        Frontend.setup()
