# PROJECT_NAME = impliedAnger_aiso
PROJECT_NAME = implied-anger

## Docker compose
up:
	LOCALUID=`id -u` LOCALGID=`id -g` \
	docker compose \
	--project-name $(PROJECT_NAME) up -d \

down:
	docker compose \
	--project-name $(PROJECT_NAME) down

build:
	LOCALUID=`id -u` LOCALGID=`id -g` \
	docker compose \
	--project-name $(PROJECT_NAME) build --no-cache --progress=plain

restart:
	docker compose --project-name $(PROJECT_NAME) restart
