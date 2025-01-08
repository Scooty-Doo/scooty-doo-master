from src.data.get import Get
from src.utils.extract import Extract
from ._outgoing import Outgoing
import asyncio

async def main():
    end_condition = False
    while not end_condition:
        print("Welcome to the Matrix.")
        wait_for_boot = 30
        print("Waiting 10 seconds to boot up the simulation.")
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
        trip_ids = Extract.Trip.ids(trips)
        linestrings = Extract.Trip.routes(trips)
        assert len(trip_ids) == len(linestrings), f"Length of trip_ids: {len(trip_ids)} != Length of trip_linestrings: {len(linestrings)}"

        bike_count = len(bike_ids)
        print(f"Number of bikes: {bike_count}")
        user_count = len(user_ids)
        print(f"Number of users: {user_count}")
        trip_count = len(trip_ids)
        print(f"Number of trips: {trip_count}")

        def generate_unique_user_bike_linestring_trips(user_ids, bike_ids, linestrings):
            """Generate unique (user_id, bike_id, linestring) trips where no 'user_id', 'bike_id', or 'linestring' repeats."""
            max_trips = min(len(user_ids), len(bike_ids), len(linestrings))
            
            for trip_index in range(max_trips):
                user_id = user_ids[trip_index]
                bike_id = bike_ids[trip_index]
                linestring = linestrings[trip_index]
                yield (user_id, bike_id, linestring)
        
        unique_trips = generate_unique_user_bike_linestring_trips(user_ids, bike_ids, linestrings)

        async def start_trips(unique_trips):
            successful_start_trips = 0
            unsuccessful_start_trips = 0
            started_trips = []
            for user_id, bike_id, linestring in unique_trips:
                print(f"Attempting to start trip for user {user_id} on bike {bike_id}")
                try: 
                    await outgoing.trips.start_trip(user_id=user_id, bike_id=bike_id)
                    successful_start_trips += 1
                    started_trips.append((user_id, bike_id, linestring))
                except Exception as e:
                    print(f"Failed to start trip for user {user_id} on bike {bike_id}: {e}")
                    unsuccessful_start_trips += 1
            return successful_start_trips, unsuccessful_start_trips, started_trips
        
        successful_start_trips, unsuccessful_start_trips, started_trips = await start_trips(unique_trips)
        print(f"Successfully started {successful_start_trips} trips.")
        print(f"Failed to start {unsuccessful_start_trips} trips.")
        print(f"Percentage of successful trips: {successful_start_trips / (successful_start_trips + unsuccessful_start_trips) * 100}%")
        assert successful_start_trips > 0, "No trips started successfully."
        end_condition = True
        print("End of simulation. End condition met.")

if __name__ == "__main__":
    asyncio.run(main())

    # NOTE: To run use:
    # python -m src.main
    # Make sure simulation is True in the if __name__ == "__main__": block in src/main.py

    #zones = get.zones(save_to_json=False, fallback=False)
    #zone_types = get.zone_types(save_to_json=False, fallback=False)
    #print(users)

    # Need more user/bike/trip data in database.

    # ändra ?limit=0 i _outgoing? hör med Martin (users)

    # NOTE: Preset environment variables are changed in docker-compose files and note /env folder.