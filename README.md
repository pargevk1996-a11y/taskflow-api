# TaskFlow API

Production-like backend portfolio project on FastAPI with layered architecture:

- `api` - HTTP endpoints and dependencies
- `services` - business logic
- `repositories` - data access
- `models` - SQLAlchemy ORM entities
- `schemas` - Pydantic request/response contracts

## Stack

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Celery
- JWT auth
- Docker / Docker Compose
- Pytest

## Run locally

1. Create env file:

```bash
cp .env.example .env
```

2. Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Start infrastructure:

```bash
docker compose up -d postgres redis
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start API:

```bash
uvicorn app.main:app --reload
```

Open docs: `http://localhost:8000/docs`

## Run tests

```bash
.venv/bin/pytest -q
```

## Auth flow

Registration endpoint:

```bash
POST /api/v1/auth/register
```

Request body:

```json
{
  "email": "user@example.com",
  "login": "my_login",
  "password": "strongpassword123",
  "confirm_password": "strongpassword123"
}
```

Successful response:

```json
{
  "message": "Hey Dude! Log in!"
}
```

Login endpoint:

```bash
POST /api/v1/auth/login
```

Swagger OAuth2 password flow uses the `username` field technically, but you must enter the account `login` there.

Successful response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "message": "Welcome Dude!"
}
```

## Celery

Worker:

```bash
celery -A app.tasks.celery_app worker --loglevel=info
```

## Project structure

The project follows strict folder layout with clear boundaries between transport layer, business logic, and persistence.

## Notes

- In some environments `passlib` may print a warning about `bcrypt` backend internals. This does not break runtime behavior.
- Before production deploy: make sure to run `alembic upgrade head` against the target database before starting the API.
