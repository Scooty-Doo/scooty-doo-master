class Serialize:
    @staticmethod
    def positions(positions: list[tuple[float, float]]) -> list[str]:
        """
        Serializes positions from tuples to a a list of "longitude:latitude" strings.
        For storage in environment file.
        """
        return ','.join([f"{longitude}:{latitude}" for (longitude, latitude) in positions])

    @staticmethod
    def bike_ids(bike_ids: list[int]) -> str:
        """
        Serializes bike ids to a comma-separated string.
        For storage in environment file.
        """
        return ','.join(map(str, bike_ids))
