
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

    class Lines:
        @staticmethod
        def startswith(lines, prefixes: list[str]):
            return [line for line in lines if line.startswith(tuple(prefixes))]

        @staticmethod
        def not_startswith(lines, prefixes: list[str]):
            return [line for line in lines if not line.startswith(tuple(prefixes))]
