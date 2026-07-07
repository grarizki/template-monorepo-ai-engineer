.PHONY: install dev-api dev-web dev lint format migrate demo test test-api test-web update docker-build docker-up docker-down start

install:
	cd apps/api && uv venv && uv pip install -r requirements.txt
	cd apps/web && pnpm install

dev-api:
	cd apps/api && . .venv/bin/activate && python -m uvicorn ai_template.server:app --reload --port 8000

dev-web:
	cd apps/web && pnpm dev

dev:
	@make -j2 dev-api dev-web

lint:
	cd apps/api && . .venv/bin/activate && ruff check . --fix && ruff format .
	pnpm biome check . --write

format:
	pnpm biome format --write apps/web/
	cd apps/api && . .venv/bin/activate && ruff format .

migrate:
	cd apps/api && alembic upgrade head

demo:
	cd apps/api && python -m ai_template.cli demo --model demo_model

test-api:
	cd apps/api && . .venv/bin/activate && python -m pytest tests/ -v

test-web:
	cd apps/web && pnpm test

test: test-api test-web

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

start: install migrate demo

update:
	cd apps/api && . .venv/bin/activate && rtk uv pip install --upgrade -r requirements.txt
	cd apps/web && pnpm update
