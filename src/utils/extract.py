
class Extract:
    class Bike:
        @staticmethod
        def ids(bikes):
            return [bike['id'] for bike in bikes]

        @staticmethod
        def positions(bikes):
            """Extracts the last position e.g. "POINT(13.06782 55.577859)" and converts to tuple."""
            def _point_to_tuple(point):
                point = point.replace("POINT(", "").replace(")", "")
                return tuple(map(float, point.split()))
            return [_point_to_tuple(bike['attributes']['last_position']) for bike in bikes]
        
    class Bikes:
        @staticmethod
        def available(bikes):
            return [bike for bike in bikes if bike['attributes']['is_available']]
    
    class User:
        @staticmethod
        def ids(users):
            return [user['id'] for user in users]
    
    class Trip:
        @staticmethod
        def ids(trips):
            return [trip['id'] for trip in trips]

        @staticmethod
        def routes(trips):
            """Extracts the route e.g. "LINESTRING(13.06782 55.57786,13.06787 55.57785)" and converts to list of tuples."""
            def _linestring_to_list(linestring):
                linestring = linestring.replace("LINESTRING(", "").replace(")", "")
                return [tuple(map(float, point.split())) for point in linestring.split(",")]
            return [_linestring_to_list(trip['attributes']['path_taken']) for trip in trips]

    class Lines:
        @staticmethod
        def startswith(lines, prefixes: list[str]):
            return [line for line in lines if line.startswith(tuple(prefixes))]

        @staticmethod
        def not_startswith(lines, prefixes: list[str]):
            return [line for line in lines if not line.startswith(tuple(prefixes))]
