from src.data.get import Get
from src.utils.extract import Extract
from ._outgoing import Outgoing
import asyncio

async def main():
    print("Welcome to the Matrix.")
    print("Waiting 10 seconds to boot up the simulation.")
    await asyncio.sleep(5)

    get = Get()
    outgoing = Outgoing(token="secret")

    is_ready = False
    while not is_ready:
        await asyncio.sleep(60)
        bikes = get.bikes(save_to_json=False, fallback=False)
        if len(bikes) > 0:
            is_ready = True
    
    bikes = get.bikes(save_to_json=False, fallback=False)

    bikes = Extract.Bikes.available(bikes)
    assert len(bikes) > 0, "No bikes available, after extraction, all are probably false."
    bike_ids = Extract.Bike.ids(bikes)
    positions = Extract.Bike.positions(bikes)

    assert len(bike_ids) == len(positions), f"Length of bike_ids: {len(bike_ids)} != Length of positions: {len(positions)}" + f"example bike: {bikes[0]}"

    users = get.users(save_to_json=False, fallback=False)
    user_ids = Extract.User.ids(users)

    trips = get.trips(save_to_json=False, fallback=False)
    trip_ids = Extract.Trip.ids(trips)
    trip_linestrings = Extract.Trip.routes(trips)
    assert len(trip_ids) == len(trip_linestrings), f"Length of trip_ids: {len(trip_ids)} != Length of trip_linestrings: {len(trip_linestrings)}"
    trip_id_linestring_map = dict(zip(trip_ids, trip_linestrings))

    bike_count = len(bike_ids)
    print(f"Number of bikes: {bike_count}")
    user_count = len(user_ids)
    print(f"Number of users: {user_count}")
    trip_count = len(trip_ids)
    print(f"Number of trips: {trip_count}")

    print(f"Starting trip for user {user_ids[0]} on bike {bike_ids[0]}")
    await outgoing.trips.start_trip(user_id=652134919185249768, bike_id=3)
    # 652134919185249768 (uneligible for trip)
    # 652134919185249742 (eligible for trip)

if __name__ == "__main__":
    asyncio.run(main())

    #zones = get.zones(save_to_json=False, fallback=False)
    #zone_types = get.zone_types(save_to_json=False, fallback=False)
    #print(users)

    # Need more user/bike/trip data in database.

    # see Makefile in root for instructions for how to run the simulation 
    # docker-compose -f docker-compose.yml -f docker-compose.simulation.yml up -d --build

    # ändra ?limit=0 i _outgoing? hör med Martin (users)

    # 1. Start the simulation.
    # 2. Get and extract users, trips, and bikes data.
    # ???
