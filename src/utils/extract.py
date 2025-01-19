# pylint: disable=too-few-public-methods
"""Module to manage the extraction of data."""

class Extract:
    """Class to manage the extraction of data."""
    class Bike:
        """Class to manage the extraction of bike data."""
        @staticmethod
        def ids(bikes):
            """Extracts the bike IDs."""
            return [bike['id'] for bike in bikes]

        @staticmethod
        def positions(bikes):
            """Extracts the last position e.g. "POINT(13.06782 55.577859)" and converts to tuple."""
            def _point_to_tuple(point):
                point = point.replace("POINT(", "").replace(")", "")
                return tuple(map(float, point.split()))
            return [_point_to_tuple(bike['attributes']['last_position']) for bike in bikes]

    class Bikes:
        """Class to manage the extraction of bikes data."""
        @staticmethod
        def available(bikes):
            """Extracts the available bikes."""
            return [bike for bike in bikes if bike['attributes']['is_available']]

    class User:
        """Class to manage the extraction of user data."""
        @staticmethod
        def ids(users):
            """Extracts the user IDs."""
            return [user['id'] for user in users]

    class Users:
        """Class to manage the extraction of users data."""
        @staticmethod
        def with_money(users):
            """Extracts the users with money."""
            return [user for user in users if user['attributes']['balance'] > 0.0]

    class Trip:
        """Class to manage the extraction of trip data."""
        @staticmethod
        def ids(trips):
            """Extracts the trip IDs."""
            return [trip['id'] for trip in trips]

        @staticmethod
        def routes(trips):
            """
            Extracts the route e.g. "LINESTRING(13.06782 55.57786,13.06787 55.57785)"
            and converts to list of tuples.
            """
            def _linestring_to_list(linestring):
                linestring = linestring.replace("LINESTRING(", "").replace(")", "")
                return [tuple(map(float, point.split())) for point in linestring.split(",")]
            return [_linestring_to_list(trip['attributes']['path_taken']) for trip in trips]

    class Lines:
        """Class to manage the extraction of lines."""
        @staticmethod
        def startswith(lines, prefixes: list[str]):
            """Extracts the lines that start with the prefixes."""
            return [line for line in lines if line.startswith(tuple(prefixes))]

        @staticmethod
        def not_startswith(lines, prefixes: list[str]):
            """Extracts the lines that do not start with the prefixes."""
            return [line for line in lines if not line.startswith(tuple(prefixes))]
