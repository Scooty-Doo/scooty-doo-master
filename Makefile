# Makefile
# Purpose: Makefile for starting the database, API, bike, and simulation containers in separate terminals.
# Usage:
#   make db           # starts database in the foreground
#   make api          # starts API in the foreground, ignoring output from db
#   make bike         # starts bike container in the foreground, ignoring output from db/api
#   make simulation   # starts simulation in the foreground, ignoring output from db/api/bike

#   make db-down      # stops database
#   make api-down     # stops API
#   make bike-down    # stops bike container
#   make simulation-down  # stops simulation

#   make db-logs      # shows logs for database
#   make api-logs     # shows logs for API
#   make bike-logs    # shows logs for bike container
#   make simulation-logs  # shows logs for simulation

# Purpose: Start all containers in the same terminal.
# Usage:
#   make main		# start all containers except simulation
#   make all		# start all containers
#   make main-down	# stop all containers except simulation
#   make all-down	# stop all containers
#   make main-logs	# show logs for all containers except simulation
#   make all-logs 	# show logs for all containers

db:
	docker-compose -f docker-compose.yml up --build db
db-down:
	docker-compose -f docker-compose.yml down
db-logs:
	docker-compose -f docker-compose.yml logs -f db
api:
	docker-compose -f docker-compose.yml up --build --no-deps api
api-down:
	docker-compose -f docker-compose.yml down
api-logs:
	docker-compose -f docker-compose.yml logs -f api
bike:
	docker-compose -f docker-compose.yml up --build --no-deps bike_hivemind
bike-down:
	docker-compose -f docker-compose.yml down
bike-logs:
	docker-compose -f docker-compose.yml logs -f bike_hivemind
frontend:
	docker-compose -f docker-compose.yml up --build --no-deps webclient-prod
frontend-down:
	docker-compose -f docker-compose.yml down
frontend-logs:
	docker-compose -f docker-compose.yml logs -f webclient-prod
simulation:
	docker-compose -f docker-compose.yml -f docker-compose.simulation.yml up --build --no-deps simulation
simulation-down:
	docker-compose -f docker-compose.yml -f docker-compose.simulation.yml down
simulation-logs:
	docker-compose -f docker-compose.yml -f docker-compose.simulation.yml logs -f simulation



main:
	make db &
	sleep 5
	make api &
	sleep 5
	make bike &
	sleep 5
	make frontend &
	sleep 5

main-down:
	make db down
	make api down
	make bike down
	make frontend down

main-logs:
	make db-logs &
	make api-logs &
	make bike-logs &
	make frontend-logs &

all:
	make main &
	sleep 5
	make simulation

all-down:
	make main down
	make simulation down

all-logs:
	make main-logs &
	make simulation-logs &

