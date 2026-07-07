# AI Template Monorepo

CLI-first monorepo template for AI/ML prototyping. FastAPI + Astro + Tailwind.

## Quick Start

```bash
# 1. Install deps
make install

# 2. Run demo (trains model + starts server)
make demo

# 3. Open docs
open http://127.0.0.1:8000/scalar
```

## Structure

```
├── apps/
│   ├── api/          # FastAPI + SQLite + Alembic
│   └── web/          # Astro + Tailwind
├── Makefile
├── docker-compose.yml
└── README.md
```

## API Endpoints (`/api/v1/`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/projects` | List projects |
| POST | `/api/v1/projects` | Create project |
| GET | `/api/v1/projects/{id}` | Get project |
| PUT | `/api/v1/projects/{id}` | Update project |
| PATCH | `/api/v1/projects/{id}` | Partial update |
| DELETE | `/api/v1/projects/{id}` | Delete project |
| GET | `/api/v1/models` | List models |
| POST | `/api/v1/models` | Create model |
| GET | `/api/v1/models/{id}` | Get model |
| PUT | `/api/v1/models/{id}` | Update model |
| PATCH | `/api/v1/models/{id}` | Partial update |
| DELETE | `/api/v1/models/{id}` | Delete model |
| GET | `/api/v1/training-scripts` | List scripts |
| POST | `/api/v1/training-scripts` | Create script |
| GET | `/api/v1/training-scripts/{id}` | Get script |
| PUT | `/api/v1/training-scripts/{id}` | Update script |
| PATCH | `/api/v1/training-scripts/{id}` | Partial update |
| DELETE | `/api/v1/training-scripts/{id}` | Delete script |
| GET | `/api/v1/deployments` | List deployments |
| POST | `/api/v1/deployments` | Create deployment |
| GET | `/api/v1/deployments/{id}` | Get deployment |
| PUT | `/api/v1/deployments/{id}` | Update deployment |
| PATCH | `/api/v1/deployments/{id}` | Partial update |
| DELETE | `/api/v1/deployments/{id}` | Delete deployment |
| POST | `/api/v1/train` | Run training |
| GET | `/api/v1/health` | Health check |

## CLI Commands

```bash
cd apps/api

python -m ai_template.cli create-project my-project
python -m ai_template.cli train my-model --epochs 50
python -m ai_template.cli migrate
python -m ai_template.cli serve
python -m ai_template.cli demo --model demo_model
python -m ai_template.cli lint
```

## Docker

```bash
docker compose up -d
# API: http://localhost:8000
# Web: http://localhost:4321
```

## Development

```bash
make dev-api    # FastAPI on :8000
make dev-web    # Astro on :4321
make lint       # Ruff check + format
make migrate    # Alembic upgrade head
```

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic, SQLite, Typer, Rich
- **Frontend:** Astro, Tailwind CSS
- **Tooling:** Ruff, Turborepo, Docker
- **Docs:** Scalar (modern Swagger replacement)
