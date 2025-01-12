from src.data.get import Get
from src.utils.extract import Extract
from ._outgoing import Outgoing
import asyncio
from time import time
from shapely.geometry import Point

# TODO: Make Get class async and await the requests in the main function.

async def main():
    end_condition = False
    while not end_condition:
        print("Welcome to the Matrix.")
        wait_for_boot = 60
        print(f"Waiting {wait_for_boot} seconds to boot up the simulation.")
        await asyncio.sleep(wait_for_boot)

        get = Get()
        outgoing = Outgoing(token="secret")
        bikes = get.bikes(save_to_json=False, fallback=False)

        bikes = Extract.Bikes.available(bikes)
        assert len(bikes) > 0, "No bikes available, after extraction, all are probably false."
        bike_ids = Extract.Bike.ids(bikes)
        positions = Extract.Bike.positions(bikes)

        assert len(bike_ids) == len(positions), f"Length of bike_ids: {len(bike_ids)} != Length of positions: {len(positions)}" + f"example bike: {bikes[0]}"

        users = get.users(save_to_json=False, fallback=False)
        users = Extract.Users.with_money(users)
        assert len(users) > 0, "No users with money."
        assert users[0]['attributes']['balance'] > 0.0, "First user has no money."
        user_ids = Extract.User.ids(users)

        trips = get.trips(save_to_json=False, fallback=False)

        bike_count = len(bike_ids)
        print(f"Number of bikes: {bike_count}")
        user_count = len(user_ids)
        print(f"Number of users: {user_count}")
        trip_count = len(trips)
        print(f"Number of trips: {trip_count}")

        def generate_unique_trips(user_ids, bike_ids, trips):
            """Generate unique (user_id, bike_id, trip_id, linestring) trips where no 'user_id', 'bike_id', or 'trip' repeats."""
            trip_ids = Extract.Trip.ids(trips)
            linestrings = Extract.Trip.routes(trips)
            assert len(trip_ids) == len(linestrings), f"Length of trip_ids: {len(trip_ids)} != Length of trip_linestrings: {len(linestrings)}"

            max_trips = min(len(user_ids), len(bike_ids), len(trip_ids))
            
            for trip_index in range(max_trips):
                user_id = user_ids[trip_index]
                bike_id = bike_ids[trip_index]
                trip_id = trip_ids[trip_index]
                linestring = linestrings[trip_index]
                yield (user_id, bike_id, trip_id, linestring)

        unique_trips = generate_unique_trips(user_ids, bike_ids, trips)
        print(f"Number of unique trips: {len(list(unique_trips))}")

        async def start_trips(unique_trips):
            successful_start_trips = 0
            unsuccessful_start_trips = 0
            started_trips = []
            for user_id, bike_id, trip_id, linestring in unique_trips:
                print(f"Attempting to start trip for user {user_id} on bike {bike_id}")
                try: 
                    response_json = await outgoing.trips.start_trip(user_id=user_id, bike_id=bike_id)
                    # print(response_json)
                    #response_json = {'data': {'id': 665303446870102746, 'type': 'trips', 'attributes': {'start_position': 'POINT(12.969383 55.586522)', 'end_position': None, 'path_taken': None, 'start_time': '2025-01-09T21:18:22.473747Z', 'end_time': None, 'start_fee': None, 'time_fee': None, 'end_fee': None, 'total_fee': None, 'created_at': '2025-01-09T21:18:22.473747Z', 'updated_at': '2025-01-09T21:18:22.473747Z'}, 'relationships': {'user': {'data': {'type': 'users', 'id': '652134919185249755'}}, 'bike': {'data': {'type': 'bikes', 'id': '66'}}, 'transaction': None}, 'links': {'self': 'http://api:8000/v1/trips/665303446870102746'}}, 'links': {'self': 'http://api:8000/v1/trips/665303446870102746'}}
                    generated_trip_id = response_json['data']['id']
                    successful_start_trips += 1
                    started_trips.append((user_id, bike_id, generated_trip_id, linestring))
                except Exception as e:
                    print(f"Failed to start trip for {user_id} on {bike_id}: {e.response.status_code}, {e.response.text}")
                    unsuccessful_start_trips += 1
            return successful_start_trips, unsuccessful_start_trips, started_trips

        successful_start_trips, unsuccessful_start_trips, started_trips = await start_trips(unique_trips)
        print(f"Successfully started {successful_start_trips} trips.")
        print(f"Failed to start {unsuccessful_start_trips} trips.")
        print(f"Percentage of successful trips: {successful_start_trips / (successful_start_trips + unsuccessful_start_trips) * 100}%")
        assert successful_start_trips > 0, "No trips started successfully."

        async def move_bikes(started_trips):
            successful_move_bikes = 0
            unsuccessful_move_bikes = 0
            moved_trips = []
            for user_id, bike_id, trip_id, linestring in started_trips:
                print(f"Attempting to move bike {bike_id} with user {user_id}")
                try:
                    await outgoing.bikes.move(bike_id=bike_id, position_or_linestring=linestring)
                    successful_move_bikes += 1
                    moved_trips.append((user_id, bike_id, trip_id, linestring))
                except Exception as e:
                    print(f"Failed to move bike {bike_id} with user {user_id}: {e}")
                    unsuccessful_move_bikes += 1
            return successful_move_bikes, unsuccessful_move_bikes, moved_trips

        successful_move_bikes, unsuccessful_move_bikes, moved_trips = await move_bikes(started_trips)
        print(f"Successfully moved {successful_move_bikes} bikes.")
        print(f"Failed to move {unsuccessful_move_bikes} bikes.")
        print(f"Percentage of successful bikes moved: {successful_move_bikes / (successful_move_bikes + unsuccessful_move_bikes) * 100}%")
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
            for user_id, bike_id, trip_id, linestring in moved_trips:
                distance_in_km = _get_distance_in_km(linestring)
                speed_in_kmh = 1000
                duration_in_seconds = _get_duration_in_seconds(distance_in_km, speed_in_kmh)
                moved_trips_with_duration.append((user_id, bike_id, trip_id, linestring, duration_in_seconds))
            return _sort_trips_by_ascending_duration(moved_trips_with_duration)
        
        sorted_moved_trips = get_moved_trips_with_duration(moved_trips)

        async def end_trips(moved_trips):
            successful_end_trips = 0
            unsuccessful_end_trips = 0
            ended_trips = []
            for user_id, bike_id, trip_id, linestring, duration in moved_trips:
                print(f"Attempting to end trip for user {user_id} on bike {bike_id}")
                try:
                    await outgoing.trips.end_trip(user_id=user_id, bike_id=bike_id, trip_id=trip_id)
                    successful_end_trips += 1
                    ended_trips.append((user_id, bike_id, trip_id, linestring))
                except Exception as e:
                    print(f"Failed to end trip for user {user_id} on bike {bike_id}: {e}")
                    unsuccessful_end_trips += 1
            return successful_end_trips, unsuccessful_end_trips, ended_trips

        def _filter_trips_by_duration(moved_trips, elapsed_seconds):
            trips_to_end_now = [trip for trip in moved_trips if trip[-1] <= elapsed_seconds]
            remaining_trips = [trip for trip in moved_trips if trip[-1] > elapsed_seconds]
            return trips_to_end_now, remaining_trips

        async def manage_trip_endings(moved_trips):
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

                moved_trips_with_margin = [(user_id, bike_id, trip_id, linestring, duration + margin_of_error) for user_id, bike_id, trip_id, linestring, duration in moved_trips]
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
                    print(f"Percentage of successful trips: {successful_end_trips / (successful_end_trips + unsuccessful_end_trips) * 100}%")
                    failed_trips.extend([trip for trip in trips_to_end_now if trip not in ended_trips])

                allowed_attempts -= 1
                total_attempts += 1

                if remaining_trips or failed_trips:
                    print(f"Remaining trips: {len(remaining_trips) + len(failed_trips)}. Waiting {sleep_period} seconds for next attempt.")
                    await asyncio.sleep(sleep_period)
                else:
                    print("All trips have been ended.")
                    break

            total_time = sleep_period * total_attempts
            assert ended_trip_count > 0, f"No trips ended successfully after {total_time} seconds and {total_attempts} attempts."
            print(f"Ended {ended_trip_count} trips successfully after {total_time} seconds and {total_attempts} attempts.")
        
        await manage_trip_endings(sorted_moved_trips)

        end_condition = True
        print("End of simulation. End condition met.")

if __name__ == "__main__":
    asyncio.run(main())

    # TODO: ändra default_speed till en environment variable för cykeln! I nuläget har jag ställt den till 1000 kmh i cykeln och här i simulation.src.main

    # NOTE: To run use:
    # python -m src.main
    # Make sure simulation is True in the if __name__ == "__main__": block in src/main.py

    #zones = get.zones(save_to_json=False, fallback=False)
    #zone_types = get.zone_types(save_to_json=False, fallback=False)
    #print(users)

    # Need more user/bike/trip data in database.

    # ändra ?limit=0 i _outgoing? hör med Martin (users)

    # NOTE: Preset environment variables are changed in docker-compose files and note /env folder.