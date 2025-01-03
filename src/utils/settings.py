import os

class Settings:

    class Directory:
        mocked_data = 'repos/backend/database/mock_data/data/generated/'
        data = 'data'
        env = 'env'
        repos = 'repos'
        class Name:
            backend = 'backend'
            frontend = 'frontend'
            bike = 'bike'
            database = 'database'
            venv = '.venv'
    
    class Filenames:
        class Mocked:
            bikes = 'bikes_with_updated_positions.csv'
            trips = 'trip_data_with_ids.csv'
            users = 'users_cleaned.csv'
            zones = 'map_zones.csv'
            zone_types = 'zone_types.csv'

    class Endpoints:
        backend_url = os.getenv("BACKEND_URL") # .env file in .env/.env
        token = os.getenv("TOKEN")
        #bike_id = os.getenv("BIKE_ID")

        # TODO: Endpoints need to get the values through parameters
        # (convert attribute to method) or environment (if BIKE_ID).

        class Bikes:
            endpoint = 'v1/bikes/'
            get_all = f'{endpoint}'
            get = f'{endpoint}' + f'/{os.getenv("BIKE_ID")}'
            add = f'{endpoint}'
            update = f'{endpoint}' + f'/{os.getenv("BIKE_ID")}'
            remove = f'{endpoint}' + f'/{os.getenv("BIKE_ID")}'

        class Trips:
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
            endpoint = 'v1/zones/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}/{{id}}'
            update = f'{endpoint}/{{id}}'
            remove = f'{endpoint}/{{id}}'
            get_parking = f'{endpoint}/parking'
            get_types = f'{endpoint}/types'

        class Users:
            endpoint = 'v1/users/'
            get_all = f'{endpoint}'
            create = f'{endpoint}'
            get = f'{endpoint}/{{id}}'