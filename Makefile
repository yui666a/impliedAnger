# PROJECT_NAME = impliedAnger_aiso
PROJECT_NAME = aiso20221209

## Docker compose
up:
	LOCALUID=`id -u` LOCALGID=`id -g` \
	docker compose \
	--project-name $(PROJECT_NAME) up -d \

down:
	docker-compose \
	--project-name $(PROJECT_NAME) down

build:
	LOCALUID=`id -u` LOCALGID=`id -g` \
	docker-compose --project-name $(PROJECT_NAME) build --no-cache

restart:
	docker-compose --project-name $(PROJECT_NAME) restart