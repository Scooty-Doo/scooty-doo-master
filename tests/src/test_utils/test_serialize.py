from src.utils.serialize import Serialize

def test_serialize_positions():
    positions = [(13.06782, 55.577859), (14.12345, 55.67890)]
    result = Serialize.positions(positions)
    assert result == "13.06782:55.577859,14.12345:55.6789", \
        "Should serialize positions as longitude:latitude pairs, comma-separated"

def test_serialize_bike_ids():
    bike_ids = [101, 102, 105]
    result = Serialize.bike_ids(bike_ids)
    assert result == "101,102,105", "Should serialize bike IDs as comma-separated string"
