up:
	docker-compose -f docker-compose.yml -f docker-compose.simulation.yml up -d --build

down:
	docker-compose -f docker-compose.yml -f docker-compose.simulation.yml down

logs:
	docker-compose -f docker-compose.yml -f docker-compose.simulation.yml logs -f

build:
	docker-compose -f docker-compose.yml -f docker-compose.simulation.yml build
