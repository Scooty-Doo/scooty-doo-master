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

def test_bikes_available():
    bikes = [
        {"id": 101, "attributes": {"is_available": True}},
        {"id": 102, "attributes": {"is_available": False}},
        {"id": 103, "attributes": {"is_available": True}}
    ]
    result = Extract.Bikes.available(bikes)
    assert result == [
        {"id": 101, "attributes": {"is_available": True}},
        {"id": 103, "attributes": {"is_available": True}}], "Should return only available bikes"

def test_user_ids():
    users = [
        {"id": 1, "attributes": {"balance": 50.0}},
        {"id": 2, "attributes": {"balance": 0.0}}
    ]
    result = Extract.User.ids(users)
    assert result == [1, 2], "Should extract user IDs correctly"

def test_users_with_money():
    users = [
        {"id": 1, "attributes": {"balance": 50.0}},
        {"id": 2, "attributes": {"balance": 0.0}},
        {"id": 3, "attributes": {"balance": 20.0}}
    ]
    result = Extract.Users.with_money(users)
    assert result == [
        {"id": 1, "attributes": {"balance": 50.0}},
        {"id": 3, "attributes": {"balance": 20.0}}], "Should return users with positive balance"

def test_trip_ids():
    trips = [
        {"id": 201, "attributes": {"path_taken": "LINESTRING(13.0 55.0,14.0 56.0)"}},
        {"id": 202, "attributes": {"path_taken": "LINESTRING(14.1 55.1,15.1 56.1)"}}
    ]
    result = Extract.Trip.ids(trips)
    assert result == [201, 202], "Should extract trip IDs correctly"

def test_trip_routes():
    trips = [
        {"id": 201, "attributes": {"path_taken": "LINESTRING(13.0 55.0,14.0 56.0)"}},
        {"id": 202, "attributes": {"path_taken": "LINESTRING(14.1 55.1,15.1 56.1)"}}
    ]
    result = Extract.Trip.routes(trips)
    assert result == [[(13.0, 55.0), (14.0, 56.0)], [(14.1, 55.1), (15.1, 56.1)]], \
        "Should convert LINESTRING to list of tuples correctly"
