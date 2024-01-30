.SILENT:
.DEFAULT_GOAL:= help

# text colors
COLOR_DEFAULT=\033[0m
COLOR_RED=\033[31m
COLOR_GREEN=\033[32m
COLOR_YELLOW=\033[33m

.PHONY: run-server
run-server: ## Run Local Server On Machine
run-server:
	@printf "$(COLOR_GREEN)\nRunning Local Server$(COLOR_DEFAULT)\n\n"
	python3 -m uvicorn app.main:app --reload


.PHONY: start
start: ## Start development environment
start:
	@printf "$(COLOR_GREEN)\nStarting development environment$(COLOR_DEFAULT)\n\n"
	docker-compose -p modulaptop_store -f dev/docker-compose.yml up -d --build


.PHONY: run-tests
.ONESHELL:
run-tests: ## Run tests On Machine
run-tests:
	export POSTGRES_SERVER=localhost
	export POSTGRES_PORT=5434
	@printf "$(COLOR_GREEN)\nRunning tests$(COLOR_DEFAULT)\n\n"
	pytest -x --doctest-modules ./tests


.PHONY: revision
revision: ## Create DB revision
revision:
	@printf "$(COLOR_GREEN)\nCreating DB revision$(COLOR_DEFAULT)\n\n"
	@echo "Enter description for a new revision: "; \
    read DESC; \
    alembic revision --autogenerate -m "$$DESC"


.PHONY: migrate
migrate: ## Run DB migrations
migrate:
	@printf "$(COLOR_GREEN)\nRunning DB migrations$(COLOR_DEFAULT)\n\n"
	alembic upgrade head


.PHONY: downgrade
downgrade: ## Downgrade the migration
downgrade:
	@printf "$(COLOR_GREEN)\nDowngrading the DB revision$(COLOR_DEFAULT)\n\n"
	@echo "Enter an integer to downgrade from current revision or the revision identifier: "; \
    read REVISION; \
    alembic downgrade "$$REVISION"
