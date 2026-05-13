COMPOSE = docker compose
.PHONY: run stop logs build rebuild migration tests


run:
	$(COMPOSE) up -d
	@echo "DB and app started successfully"

stop:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f app

build:
	$(COMPOSE) build

rebuild:
	$(COMPOSE) up -d --build

# Cmd to make new migrations. Requires msg variable to be provided during executiion
migration:
	alembic revision --autogenerate -m "$(msg)"

# Cmd to perfrom tests
tests:
	pytest -v -s