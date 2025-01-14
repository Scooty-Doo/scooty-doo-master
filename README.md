[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-master/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-master/?branch=main)
[![Code Coverage](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-master/badges/coverage.png?b=main)](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-master/?branch=main)
[![Build Status](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-master/badges/build.png?b=main)](https://scrutinizer-ci.com/g/Scooty-Doo/scooty-doo-master/build-status/main)

# scooty-doo-master
### ***Master repository for the Scooty-Doo application.***

#### *Setup:*
```python
python -m src.setup._venv
```

This will setup a virtual environment and install dependencies.
You can also run:

```python
python -m src.main
```

...and setup will happen automatically.

#### *Running the master application:*

- **Run using the main module.**  
    When we run using the main module we can select which branch (and commit hash) we want to use for each repository.

    We can also select a simulation speed factor. If the simulation speed factor is set at 1000 then the bikes will travel at 2 000 km/h (since the default speed is 20 km/h). 

    We can also choose if we want to rebuild when we run the system. If rebuild is True then we will pull the latest changes for each repo, though branch and commit hash settings will still apply. The frontend will also rebuild (npm install + npm build).

    At the bottom we set SIMULATION to True or False depending if we want to run the simulation along with the regular services (database, api, frontend, bike). 

    ```python
    python -m src.main
    ```

    ```python
    # src/main.py

    if __name__ == "__main__":
        main = Main(
            use_submodules=False,
            backend_branch='main',
            backend_commit=None,
            frontend_branch='main',
            frontend_commit=None,
            bike_branch='main',
            bike_commit=None
        )

        options = {
            "simulation_speed_factor": 1000.0,
            "rebuild": True,
            "open_chrome_tabs": False
            }

        SIMULATION = True

        if SIMULATION:
            main.simulate(**options)
        if not SIMULATION:
            main.run(**options)

    # python -m src.main
    ```

- **Run using the Makefile commands.**  
    This option only works if you already have setup the master environment setup. If not then you can use:

    ```python
    python -m src.setup._venv
    ```

    This essentially creates a virtual environment and installs dependencies for the master repository.

    Makefile commands are just abbreviated docker-compose commands. The up commands are:

    ```python
    # Running in separate terminals
    make db
    make api
    make bike
    make frontend
    make simulation

    # Running in one terminal
    make main # db, api, bike, frontend
    make all  # db, api, bike, frontend, simulation
    ```

    If you want to down a given container or group of containers you add "-down" behind the up-command. For example:


    ```python
    # Running in separate terminals
    make db-down
    make api-down
    make bike-down
    make frontend-down
    make simulation-down

    # Running in one terminal
    make main-down # db, api, bike, frontend
    make all-down  # db, api, bike, frontend, simulation
    ```
    You can also do "-logs" for example (make db-logs) if you want to show logs.

    NOTE: Make is included on Linux and Mac systems. If you are using Windows you can install Make first or use the docker-compose commands specified in the Makefile in the root of the master repository.
    ```python
    # Makefile

    # e.g.
    up:
        docker-compose -f docker-compose.yml up --build db
        # copy the above line
    ```

    If you want to change simulation speed factor when running the system using Makefile commands you need to manually change the DEFAULT_SPEED environment of the *bike_hivemind* service in *docker-compose.yml*. Keep in mind that the DEFAULT_SPEED environment variable in docker-compose.yml will update whenever you run the main module (so any manual changes will be overwritten).