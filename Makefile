## ARGS
PROJECT_NAME=implied-anger
# $(eval UID := $(shell id -u))
# $(eval GID ?= $(shell id -g))

## Docker compose
up:
	LOCALUID=`id -u` LOCALGID=`id -g` \
	docker compose --project-name $(PROJECT_NAME) \
	--env-file ./.env \
	up -d 

down:
	docker compose --project-name $(PROJECT_NAME) down

build:
	LOCALUID=`id -u` LOCALGID=`id -g` \
	docker compose --project-name $(PROJECT_NAME) \
	build --no-cache --progress=plain

restart:
	docker compose --project-name $(PROJECT_NAME) restart
