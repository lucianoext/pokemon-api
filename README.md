# Pokemon API

A FastAPI-based Pokémon management system for Pokemon, trainers, teams and backpacks using a layered architecture in Python.

## Project Overview

The **Pokémon API** is a RESTful backend designed to manage trainers, Pokémon, items, teams, and inventories.
It uses **FastAPI**, **SQLModel/SQLAlchemy**, a well‑structured **Clean Architecture** approach to ensure scalability and maintainability and Alembic migrations for database schema management.

## Features

### Trainers
- Create and manage Pokémon trainers
- Manage trainer backpacks and team composition

### Pokémon
- Add and manage Pokémon with:
  - Types
  - Stats
  - Nature
  - Attacks
  - Levels

### Items & Backpack
- Manage items with pricing
- Track trainer inventory
- Modify item quantities

### Teams
- Manage trainer teams (max 6 Pokémon)
- Swap Pokémon
- Validate limits

## Architecture

This project follows **Clean Architecture**, separating concerns into clear layers:

``

src/
├── api/               # FastAPI routers and request/response handling
├── core/              # Configurations and settings
├── persistence/        # Database models and repositories
├── services/           # Business logic layer
├── schemas/            # Pydantic/SQLModel schemas
└── main.py             # Application entrypoint

### Layers
- **Models** → SQLAlchemy/SQLModel entities
- **Schemas** → Pydantic request/response validators
- **Repositories** → Data access abstraction
- **Services** → Domain/business logic
- **API Routes** → Versioned REST endpoints

---

## Technologies
- **Language:** Python 3.10+
- **Framework:** FastAPI (app entry: [main.py](main.py))
- **ORM:** SQLModel  (models: [src/persistence/database/models.py](src/persistence/database/models.py))
- **Containers:** Docker / Docker Compose ([Dockerfile](Dockerfile), [docker-compose.yaml](docker-compose.yaml))

## Repository Structure (key files)
- **Entry:** [main.py](main.py)
- **Config:** [src/config.py](src/config.py)
- **API routes:** [src/presentation/api/pokemon.py](src/presentation/api/pokemon.py), [src/presentation/api/trainers.py](src/presentation/api/trainers.py), [src/presentation/api/items.py](src/presentation/api/items.py), [src/presentation/api/teams.py](src/presentation/api/teams.py), [src/presentation/api/backpacks.py](src/presentation/api/backpacks.py)
- **Services:** [src/application/services](src/application/services)
- **DTOs:** [src/application/dtos](src/application/dtos)
- **Domain entities:** [src/domain/entities](src/domain/entities)
- **Persistence / Repositories:** [src/persistence/repositories](src/persistence/repositories)
- **Seed script:** [scripts/seed_data.py](scripts/seed_data.py)

## Requirements
- **Dependencies:** see `dependencias_actuales.txt`
- **Dev dependencies:** see `dependencias_dev.txt`

## Getting Started (Docker — recommended)

This project is set up to run with Docker Compose. The Docker-first workflow ensures the app, database and other services run consistently across machines.

### Prerequisites
- Docker
- Docker Compose (v2 recommended)

### Quick start
```bash
# clone
git clone <your-repo-url>  # or use your existing local copy
cd pokemon-api

# create a `.env` file with your database connection string if you want to use other database
DATABASE_URL=postgresql://username:password@host:port/database

# start the app and related services
docker compose up --build

# Run database migrations:
docker compose exec api alembic upgrade head
```

By default the API will be available at:

- http://localhost:8000
- OpenAPI docs: http://localhost:8000/docs

### Dev mode (hot reload)
If your compose file includes a development service or profile (common names: `dev`, `pokemon-api-dev`, or `pokemon-api`), run:

```bash
docker compose --profile dev up --build
```

or start only the API service (if named `pokemon-api`):

```bash
docker compose up --build pokemon-api
```

### Seed the database
If a seed service exists (e.g. `pokemon-seed`) you can run:

```bash
docker compose run --rm pokemon-seed
```

(Check `docker-compose.yaml` for the exact service name used in this repository.)

### Common Docker commands

```bash
# Rebuild images
docker compose build --no-cache

# Run in background
docker compose up -d

# Show logs
docker compose logs -f

# Stop and remove containers
docker compose down
```

## Local development (optional)
If you prefer running locally without Docker, create a virtualenv and install dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate

pip install -r dependencias_actuales.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API docs: http://127.0.0.1:8000/docs

---

## Models & DTOs
- **Persistence models:** [src/persistence/database/models.py](src/persistence/database/models.py)
- **Domain entities examples:** [src/domain/entities/pokemon.py](src/domain/entities/pokemon.py), [src/domain/entities/trainer.py](src/domain/entities/trainer.py)
- **DTOs:** [src/application/dtos/pokemon_dto.py](src/application/dtos/pokemon_dto.py), [src/application/dtos/trainer_dto.py](src/application/dtos/trainer_dto.py)

## Endpoints summary
- **Pokémon:** CRUD and queries — see [src/presentation/api/pokemon.py](src/presentation/api/pokemon.py)
- **Trainers:** CRUD — see [src/presentation/api/trainers.py](src/presentation/api/trainers.py)
- **Items / Backpacks / Teams:** see respective files under [src/presentation/api](src/presentation/api)

## Persistence
- **Connection / session:** [src/persistence/database/connection.py](src/persistence/database/connection.py)
- **SQLAlchemy repositories:** [src/persistence/repositories](src/persistence/repositories)

## Running Migrations

### To create a new migration:

```bash
docker compose exec api alembic revision --autogenerate -m "description of changes"
```

To apply migrations:

```bash
docker compose exec api alembic upgrade head
```

To rollback migrations:

```bash
docker compose exec api alembic downgrade -1
```

## Scripts
- **Seed DB:** [scripts/seed_data.py](scripts/seed_data.py)

## Contribution
- Open issues or PRs; follow the project layering and style.

## Database Schema

For detailed information about the database schema and relationships, see [Database Diagrams](docs/Mermaid Chart.png).
