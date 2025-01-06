from src.data.get import Get

if __name__ == "__main__":
    print("Welcome to the Matrix.")

    get = Get()
    bikes = get.bikes(save_to_json=False, fallback=False)
    print(bikes)


    # see Makefile in root for instructions for how to run the simulation 