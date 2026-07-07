.PHONY: install dev-api dev-web dev lint migrate demo docker-build docker-up docker-down start

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
	cd apps/api && ruff check . --fix && ruff format .

migrate:
	cd apps/api && alembic upgrade head

demo:
	cd apps/api && python -m ai_template.cli demo --model demo_model

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

start: install migrate demo
