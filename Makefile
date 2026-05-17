COMPOSE = docker compose
.PHONY: run stop logs migration tests pull


run:
	$(COMPOSE) up -d
	@echo "DB and app started successfully"

stop:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f app

# Pull latest app image from Docker Hub
pull:
	docker pull foxxxy315/todolist-app:latest


# Cmd to make new migrations. Requires msg variable to be provided during executiion
migration:
	alembic revision --autogenerate -m "$(msg)"

# Cmd to perfrom tests
tests:
	python3 -m pytest -v -s