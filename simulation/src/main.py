# pylint: disable=line-too-long

import asyncio
import os
from time import time
import jwt # pylint: disable=import-error
from shapely.geometry import Point # pylint: disable=import-error
from src.data.get import Get # pylint: disable=import-error, no-name-in-module
from src.utils.extract import Extract # pylint: disable=import-error, no-name-in-module
from ._outgoing import Outgoing

TOKEN = os.getenv("TOKEN")
LIMIT = os.getenv("BIKE_LIMIT")
JWT_SECRET = os.getenv("JWT_SECRET")
TRIPS_LIMIT = int(os.getenv("TRIPS_LIMIT"))

async def main(): # pylint: disable=too-many-locals, too-many-statements
    end_condition = False
    while not end_condition:
        print("Welcome to the Matrix.")

        get = Get()
        outgoing = Outgoing(token=TOKEN)
        bikes = await get.bikes(save_to_json=False, limit=LIMIT)

        bikes = Extract.Bikes.available(bikes)
        assert len(bikes) > 0, "No bikes available, after extraction, all are probably false."
        bike_ids = Extract.Bike.ids(bikes)
        positions = Extract.Bike.positions(bikes)

        assert len(bike_ids) == len(positions), \
            f"Length of bike_ids: {len(bike_ids)} != Length of positions: {len(positions)}" + \
                f"example bike: {bikes[0]}"

        users = await get.users(save_to_json=False, limit=LIMIT)
        user_ids = Extract.User.ids(users)

        trips = await get.trips(save_to_json=False, limit=LIMIT)

        bike_count = len(bike_ids)
        print(f"Number of bikes: {bike_count}")
        user_count = len(user_ids)
        print(f"Number of users: {user_count}")
        trip_count = len(trips)
        print(f"Number of trips: {trip_count}")

        def generate_unique_trips(user_ids, bike_ids, trips):
            """
            Generate unique (user_id, bike_id, trip_id, linestring) trips 
            where no 'user_id', 'bike_id', or 'trip' repeats."""
            trip_ids = Extract.Trip.ids(trips)
            linestrings = Extract.Trip.routes(trips)
            assert len(trip_ids) == len(linestrings), \
                f"Length of trip_ids: {len(trip_ids)} != Length of trip_linestrings: {len(linestrings)}"

            max_trips = min(len(user_ids), len(bike_ids), len(trip_ids))

            trips = []
            for trip_index in range(max_trips):
                token = jwt.encode({"sub": user_ids[trip_index], "scopes": ["user"]}, JWT_SECRET, "HS256")
                user_id = user_ids[trip_index]
                bike_id = bike_ids[trip_index]
                trip_id = trip_ids[trip_index]
                linestring = linestrings[trip_index]
                trips.append((user_id, token, bike_id, trip_id, linestring))
            return trips

        unique_trips = generate_unique_trips(user_ids, bike_ids, trips)
        print(f"Number of unique trips: {len(list(unique_trips))}")

        print(f"Simulating: {TRIPS_LIMIT} trips")
        unique_trips = unique_trips[:TRIPS_LIMIT]

        async def start_trips(unique_trips):
            successful_start_trips = 0
            unsuccessful_start_trips = 0
            started_trips = []
            for user_id, token, bike_id, trip_id, linestring in unique_trips: # pylint: disable=unused-variable
                print(f"Attempting to start trip for user {user_id} on bike {bike_id}")
                try:
                    response_json = await outgoing.trips.start_trip(token=token, bike_id=bike_id, user_id=user_id)
                    generated_trip_id = response_json['data']['id']
                    successful_start_trips += 1
                    started_trips.append((user_id, token, bike_id, generated_trip_id, linestring))
                    await asyncio.sleep(0.001)
                except Exception as e:
                    print(f"Failed to start trip for {user_id} on {bike_id}: {e}")
                    unsuccessful_start_trips += 1
            return successful_start_trips, unsuccessful_start_trips, started_trips

        successful_start_trips, unsuccessful_start_trips, started_trips = await start_trips(unique_trips)
        print(f"Successfully started {successful_start_trips} trips.")
        print(f"Failed to start {unsuccessful_start_trips} trips.")
        if successful_start_trips == 0:
            print("No trips started successfully.")
        else:
            print(
                f"Percentage of successful trips: "
                    f"{successful_start_trips / (successful_start_trips + unsuccessful_start_trips) * 100}%")
        assert successful_start_trips > 0, "No trips started successfully."
        async def move_bikes(started_trips):
            successful_move_bikes = 0
            unsuccessful_move_bikes = 0
            moved_trips = []
            for user_id, token, bike_id, trip_id, linestring in started_trips:
                print(f"Attempting to move bike {bike_id} with user {user_id}")
                try:
                    await outgoing.bikes.move(bike_id=bike_id, position_or_linestring=linestring)
                    successful_move_bikes += 1
                    moved_trips.append((user_id, token, bike_id, trip_id, linestring))
                    await asyncio.sleep(0.001)
                except Exception as e:
                    print(f"Failed to move bike {bike_id} with user {user_id}: {e}")
                    unsuccessful_move_bikes += 1
            return successful_move_bikes, unsuccessful_move_bikes, moved_trips

        successful_move_bikes, unsuccessful_move_bikes, moved_trips = await move_bikes(started_trips)
        print(f"Successfully moved {successful_move_bikes} bikes.")
        print(f"Failed to move {unsuccessful_move_bikes} bikes.")
        print(
            f"Percentage of successful bikes moved: "
                f"{successful_move_bikes / (successful_move_bikes + unsuccessful_move_bikes) * 100}%")
        assert successful_move_bikes > 0, "No bikes moved successfully."

        def get_moved_trips_with_duration(moved_trips):
            def _get_distance_in_km(linestring):
                def _convert_to_kilometers(distance):
                    return distance / 1000
                start_point = Point(linestring[0])
                end_point = Point(linestring[-1])
                distance = start_point.distance(end_point)
                return _convert_to_kilometers(distance)

            def _get_duration_in_seconds(distance_in_km, speed_in_kmh):
                return (distance_in_km / speed_in_kmh) * 3600

            def _sort_trips_by_ascending_duration(trips_with_duration):
                return sorted(trips_with_duration, key=lambda x: x[-1])

            moved_trips_with_duration = []
            for user_id, token, bike_id, trip_id, linestring in moved_trips:
                distance_in_km = _get_distance_in_km(linestring)
                speed_in_kmh = 1000
                duration_in_seconds = _get_duration_in_seconds(distance_in_km, speed_in_kmh)
                moved_trips_with_duration.append(
                    (user_id, token, bike_id, trip_id, linestring, duration_in_seconds))
            return _sort_trips_by_ascending_duration(moved_trips_with_duration)

        sorted_moved_trips = get_moved_trips_with_duration(moved_trips)

        async def end_trips(moved_trips):
            successful_end_trips = 0
            unsuccessful_end_trips = 0
            ended_trips = []
            for user_id, token, bike_id, trip_id, linestring, duration in moved_trips: # pylint: disable=unused-variable
                print(f"Attempting to end trip for user {user_id} on bike {bike_id}")
                try:
                    await outgoing.trips.end_trip(user_id=user_id, bike_id=bike_id, trip_id=trip_id, token=token)
                    successful_end_trips += 1
                    ended_trips.append((user_id, bike_id, trip_id, linestring))
                    await asyncio.sleep(0.001)
                except Exception as e:
                    print(f"Failed to end trip for user {user_id} on bike {bike_id}: {e}")
                    unsuccessful_end_trips += 1
            return successful_end_trips, unsuccessful_end_trips, ended_trips

        def _filter_trips_by_duration(moved_trips, elapsed_seconds):
            trips_to_end_now = [trip for trip in moved_trips if trip[-1] <= elapsed_seconds]
            remaining_trips = [trip for trip in moved_trips if trip[-1] > elapsed_seconds]
            return trips_to_end_now, remaining_trips

        async def manage_trip_endings(moved_trips): # pylint: disable=too-many-locals
            start_time = time()
            active_trip_count = len(moved_trips)
            ended_trip_count = 0
            allowed_attempts = 12
            sleep_period = 20
            total_attempts = 0
            margin_of_error = 10

            failed_trips = []

            while ended_trip_count < active_trip_count and allowed_attempts > 0:
                elapsed_seconds = int(time() - start_time)
                print(f"Elapsed time: {elapsed_seconds} seconds.")

                moved_trips_with_margin = [
                    (user_id, token, bike_id, trip_id, linestring, duration + margin_of_error) \
                        for user_id, token, bike_id, trip_id, linestring, duration in moved_trips]
                moved_trips_with_margin.extend(failed_trips)
                failed_trips = []
                trips_to_end_now, remaining_trips = _filter_trips_by_duration(moved_trips_with_margin, elapsed_seconds)
                if not trips_to_end_now:
                    print(f"No trips ready to end at {elapsed_seconds} seconds.")
                else:
                    print(f"Attempting to end {len(trips_to_end_now)} trips at {elapsed_seconds} seconds.")
                    successful_end_trips, unsuccessful_end_trips, ended_trips = await end_trips(trips_to_end_now)
                    print(f"Successfully ended {successful_end_trips} trips.")
                    print(f"Failed to end {unsuccessful_end_trips} trips.")
                    ended_trip_count += successful_end_trips
                    print(
                        f"Percentage of successful trips: "
                            f"{successful_end_trips / (successful_end_trips + unsuccessful_end_trips) * 100}%")
                    failed_trips.extend([trip for trip in trips_to_end_now if trip not in ended_trips])

                allowed_attempts -= 1
                total_attempts += 1

                if remaining_trips or failed_trips:
                    print(
                        f"Remaining trips: "
                            f"{len(remaining_trips) + len(failed_trips)}. Waiting {sleep_period} seconds for next attempt.")
                    await asyncio.sleep(sleep_period)
                else:
                    print("All trips have been ended.")
                    break

            total_time = sleep_period * total_attempts
            assert ended_trip_count > 0, \
                f"No trips ended successfully after {total_time} seconds and {total_attempts} attempts."
            print(f"Ended {ended_trip_count} trips successfully after "
                  f"{total_time} seconds and {total_attempts} attempts.")

        await manage_trip_endings(sorted_moved_trips)

        end_condition = True
        print("End of simulation. End condition met.")

if __name__ == "__main__": # pragma: no cover
    asyncio.run(main())
