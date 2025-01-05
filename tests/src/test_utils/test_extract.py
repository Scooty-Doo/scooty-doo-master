from src.utils.extract import Extract

def test_bike_ids_extraction():
    bikes = [
        {"id": 101, "attributes": {"last_position": "POINT(13.06782 55.577859)"}},
        {"id": 102, "attributes": {"last_position": "POINT(14.12345 55.67890)"}}
    ]
    result = Extract.Bike.ids(bikes)
    assert result == [101, 102], "Should extract the bike IDs correctly"

def test_bike_positions_extraction():
    bikes = [
        {"id": 101, "attributes": {"last_position": "POINT(13.06782 55.577859)"}},
        {"id": 102, "attributes": {"last_position": "POINT(14.12345 55.67890)"}}
    ]
    result = Extract.Bike.positions(bikes)
    assert result == [(13.06782, 55.577859), (14.12345, 55.67890)], \
        "Should parse 'POINT(lon lat)' string into float tuples correctly"

def test_lines_startswith():
    lines = ["LORD=123", "GOD=456", "LORDGOD=789"]
    result = Extract.Lines.startswith(lines, ["LORD"])
    assert result == ["LORD=123", "LORDGOD=789"]

def test_lines_not_startswith():
    lines = ["LORD=123", "GOD=456", "LORDGOD=789"]
    result = Extract.Lines.not_startswith(lines, ["LORD"])
    assert result == ["GOD=456"]
