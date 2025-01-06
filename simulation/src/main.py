from src.data.get import Get

if __name__ == "__main__":
    print("Welcome to the Matrix.")

    get = Get()
    bikes = get.bikes(save_to_json=False, fallback=False)
    users = get.users(save_to_json=False, fallback=False)
    trips = get.trips(save_to_json=False, fallback=False)
    zones = get.zones(save_to_json=False, fallback=False)
    zone_types = get.zone_types(save_to_json=False, fallback=False)
    print(users)


    # see Makefile in root for instructions for how to run the simulation 

    # 1. Start the simulation.
    # 2. Get and extract users, trips, and bikes data.
    # ???