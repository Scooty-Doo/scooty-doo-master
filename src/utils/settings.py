# pylint: disable=too-few-public-methods
"""Module to manage the settings of the project."""

import os

class Settings:
    """Class to manage the settings of the project."""
    class Directory:
        """Class to manage the directories of the project."""
        mocked_data = 'repos/backend/database/mock_data/data/generated/'
        data = 'data'
        env = 'env'
        logs = 'logs'
        repositories = os.getenv("REPOSITORIES_DIRECTORY", 'repositories')
        local_repositories = 'repositories'
        class Name:
            """Class to manage the names of the directories of the project."""
            backend = 'backend'
            frontend = 'frontend'
            bike = 'bike'
            database = 'database'
            venv = '.venv'
            submodules = 'submodules'

    class Filenames:
        """Class to manage the filenames of the project."""
        class Mocked:
            """Class to manage the mocked filenames of the project."""
            bikes = 'bikes_with_updated_positions.csv'
            trips = 'trip_data_with_ids.csv'
            users = 'users_cleaned.csv'
            zones = 'map_zones.csv'
            zone_types = 'zone_types.csv'

    class Endpoints:
        """Class to manage the endpoints of the project."""
        backend_url = os.getenv("BACKEND_URL") # .env file in .env/.env
        token = os.getenv("TOKEN")
        #bike_id = os.getenv("BIKE_ID")

        # NOTE: Endpoints need to get the values through parameters
        # (convert attribute to method) or environment (if BIKE_ID).

        class Bikes:
            """Class to manage the bikes endpoints of the project."""
            endpoint = 'v1/bikes/'
            get_all = f'{endpoint}'
            get = f'{endpoint}' + f'/{os.getenv("BIKE_ID")}'
            add = f'{endpoint}'
            update = f'{endpoint}' + f'/{os.getenv("BIKE_ID")}'
            remove = f'{endpoint}' + f'/{os.getenv("BIKE_ID")}'

        class Trips:
            """Class to manage the trips endpoints of the project."""
            endpoint = 'v1/trips/'
            get_all = f'{endpoint}'
            start = f'{endpoint}'
            get = f'{endpoint}/{{id}}'
            update = f'{endpoint}/{{id}}'
            remove = f'{endpoint}/{{id}}'
            get_for_bike = f'{endpoint}/bike/{{id}}'
            get_trip_for_bike = f'{endpoint}/bike/{{id}}/trip/{{trip_id}}'
            get_user_history = f'{endpoint}/user/{{id}}'

        class Zones:
            """Class to manage the zones endpoints of the project."""
            endpoint = 'v1/zones/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}/{{id}}'
            update = f'{endpoint}/{{id}}'
            remove = f'{endpoint}/{{id}}'
            get_parking = f'{endpoint}/parking'
            get_types = f'{endpoint}/types'

        class Users:
            """Class to manage the users endpoints of the project."""
            endpoint = 'v1/users/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}/{{id}}'
