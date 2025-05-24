DOCKER_COMPOSE := docker-compose -f docker-compose.yml
DOCKER_COMPOSE_DEV := docker-compose -f docker-compose-dev.yml
PYTEST := docker exec -it lu-api-dev pytest
ALEMBIC := docker exec -it lu-api-dev alembic

migrate:
	@${ALEMBIC} upgrade head

build:
	@${DOCKER_COMPOSE} build

up:
	@${DOCKER_COMPOSE} up

down:
	@${DOCKER_COMPOSE} down --remove-orphans

full:
	@${DOCKER_COMPOSE} build
	@${DOCKER_COMPOSE} up
	@${ALEMBIC} upgrade head

test: 
	@${PYTEST}

build-dev:
	@${DOCKER_COMPOSE_DEV} build

up-dev:
	@${DOCKER_COMPOSE_DEV} up

down-dev:
	@${DOCKER_COMPOSE_DEV} down --remove-orphans

full-dev:
	@${DOCKER_COMPOSE_DEV} build
	@${DOCKER_COMPOSE_DEV} up
	@${ALEMBIC} upgrade head

test-dev: 
	@${PYTEST}