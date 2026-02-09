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
- **Dependencies:** see `dependencies.txt`
- **Dev dependencies:** see `dependencies_dev.txt`

## Getting Started (Docker — recommended)

This project is set up to run with Docker Compose. The Docker-first workflow ensures the app, database and other services run consistently across machines.

### Prerequisites
- Docker
- Docker Compose (v2 recommended)

### Quick start
```bash
# clone
git clone https://github.com/lucianoext/pokemon-api.git
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
If you prefer running locally without Docker, this project recommends using `uv` (astral-sh/uv) to manage and run pinned dependencies — the same tool used in the `Dockerfile` and `docker-compose.yaml`.

1) Install `uv` (recommended via `pipx`):

```bash
python -m pip install --user pipx
python -m pipx ensurepath
pipx install uv
```

2) Sync and install dependencies (recommended):

```bash
# install production deps
uv sync --no-dev

# install development deps (tests, linting)
uv sync --dev
```

3) Run the app with `uv` (uses the installed environment):

```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

4) Run tests and linting via `uv` groups (defined in `pyproject.toml`):

```bash
uv run --group test pytest -v
uv run --group linting ruff check src
uv run --group linting mypy src
```

Fallback (pip)

If you don't want to install `uv`, you can use a virtual environment and `pip` as a fallback:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# Windows CMD
.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate

pip install -r dependencies.txt
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


## Authentication
This API uses JWT bearer tokens for authentication. Main auth endpoints are under the `/auth` prefix:

- `POST /auth/register` — register a new user (see `UserRegistrationDTO` in `src/application/dtos/auth_dto.py`).
- `POST /auth/login` — authenticate and receive access/refresh tokens (`LoginResponseDTO`).
- `GET /auth/me` — return current authenticated user's info (requires `Authorization: Bearer <token>`).
- `PUT /auth/change-password` — change password for the authenticated user.

Example: login and use token with curl

```bash
# login
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "ash", "password": "pikachu123"}' \
  | jq

# use returned access_token in Authorization header
curl -s http://localhost:8000/auth/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

See `src/application/dtos/auth_dto.py` for DTO shapes and `src/presentation/dependencies/auth.py` for the dependency that extracts the current user from the token.

## Environment & Configuration
Configuration is loaded from environment variables (see `src/config.py` and the `.env` file support). Important variables:

- `DATABASE_URL` — SQLAlchemy/SQLModel database URL (default: `sqlite:///./app.db`).
- `JWT_SECRET_KEY` — secret for signing JWTs (keep secret in production).
- `JWT_ALGORITHM` — algorithm used for JWT (default `HS256`).
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` — access token TTL.

Create a `.env` file in the project root to override defaults when running locally or in CI.

## Tests
Unit and integration tests are in the `tests/` folder. You can run tests in one of two ways:

1) Using `pytest` directly (install test dependencies):

```bash
python -m pip install pytest pytest-asyncio pytest-cov httpx polyfactory pytest-mock
pytest -v
```

2) If you use `hatch` (project uses hatch tooling in `pyproject.toml`), run the test dependency group:

```bash
hatch run -g test pytest -v
```

After running, an HTML coverage report is produced (see pytest config in `pyproject.toml`); open `htmlcov/index.html` to view.

## Streamlit frontend
A Streamlit frontend is provided under the `frontend/` folder. The main entrypoint is `frontend/main.py` and frontend-specific dependencies are listed in `frontend/requirements.txt`.

Run locally:

```bash
pip install -r frontend/requirements.txt
streamlit run frontend/main.py
```

If you run the project with Docker Compose in dev profile the `streamlit` service will start automatically on port `8501` (see `docker-compose.yaml`).

## Database migrations
This repository uses Alembic for migrations. If you modify models, generate and apply migrations:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## Schema diagram (Mermaid)
You can visualize the main persistence models with the following Mermaid class diagram (supported by many Markdown renderers):

```mermaid
classDiagram
    class TrainerModel {
        int id
        string name
        string gender
        string region
    }

    class PokemonModel {
        int id
        string name
        string type_primary
        string type_secondary
        string attacks
        string nature
        int level
    }

    class TeamModel {
        int id
        int trainer_id
        int pokemon_id
        int position
        bool is_active
    }

    class ItemModel {
        int id
        string name
        string type
        string description
        int price
    }

    class BackpackModel {
        int id
        int trainer_id
        int item_id
        int quantity
    }

    class UserModel {
        int id
        string username
        string email
        string hashed_password
        bool is_active
        bool is_superuser
        datetime created_at
        datetime updated_at
        int trainer_id
    }

    class RefreshTokenModel {
        int id
        string token
        int user_id
        datetime expires_at
        datetime created_at
        bool is_revoked
    }

    class BattleModel {
        int id
        int team1_trainer_id
        int team2_trainer_id
        int winner_trainer_id
        float team1_strength
        float team2_strength
        float victory_margin
        datetime battle_date
        string battle_details
        datetime created_at
    }

    %% Core Pokemon relationships
    TrainerModel ||--o{ TeamModel : has
    PokemonModel ||--o{ TeamModel : appears_in
    TrainerModel ||--o{ BackpackModel : owns
    ItemModel ||--o{ BackpackModel : stored_in

    %% Authentication relationships
    UserModel ||--o| TrainerModel : controls
    UserModel ||--o{ RefreshTokenModel : has_tokens

    %% Battle relationships
    TrainerModel ||--o{ BattleModel : participates_as_team1
    TrainerModel ||--o{ BattleModel : participates_as_team2
    TrainerModel ||--o{ BattleModel : wins
```

---


## Database Schema

For detailed information about the database schema and relationships, see [Database Diagrams](docs/mermaid_chart.png)
