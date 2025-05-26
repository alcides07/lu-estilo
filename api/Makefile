include .env
.PHONY: migrations 

DOCKER_COMPOSE := docker-compose -f docker-compose.yml
DOCKER_COMPOSE_DEV := docker-compose -f docker-compose-dev.yml
PYTEST := docker exec -it lu-api-dev pytest
ALEMBIC := docker exec -it lu-api-dev alembic
API_BASH_DEV := docker exec -it lu-api-dev /bin/bash
DB_BASH_DEV := docker exec -it lu-db-dev /bin/bash

psql-dev:
	@$(DB_BASH_DEV) -c "psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)"

migrations:
	@${ALEMBIC} revision --autogenerate -m "${m}"

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

test: 
	@${PYTEST}

bash-dev:
	@${API_BASH_DEV} 

build-dev:
	@${DOCKER_COMPOSE_DEV} build

up-dev:
	@${DOCKER_COMPOSE_DEV} up

down-dev:
	@${DOCKER_COMPOSE_DEV} down --remove-orphans

full-dev:
	@${DOCKER_COMPOSE_DEV} build
	@${DOCKER_COMPOSE_DEV} up

