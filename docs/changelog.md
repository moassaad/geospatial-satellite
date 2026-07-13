# Changelog

## Sprint 03 - SQLAlchemy Database

- Added `sqlalchemy` and `psycopg2-binary` to `requirements.txt`.
- Created `app/database/base.py` with a SQLAlchemy 2.0 `DeclarativeBase`.
- Created `app/database/database.py` with engine, `SessionLocal`, and `get_db` dependency for session management.
- Added `docs/database.md` covering engine configuration, session usage, and environment variables.

## Sprint 02 - Docker Environment

- Added `Dockerfile` to containerize the FastAPI application.
- Added `.dockerignore` to keep the Docker build context minimal.
- Updated `docker-compose.yml` to run both the `app` and `db` services.
- Added an explicit `satellite_network` bridge network and `postgres_data` volume.
- Added `docs/docker.md` with Docker Compose usage instructions.

## Sprint 01 - Application Configuration

- Added `pydantic-settings` to `requirements.txt`.
- Created `app/config/settings.py` using Pydantic Settings.
- Added `.env` and updated `.env.example` to include `APP_NAME` and `DATABASE_URL`.
- Wired `settings.app_name` into the FastAPI application title in `app/main.py`.
- Added `docs/configuration.md` describing environment-based configuration.

## Sprint 00 - Project Bootstrap

- Created project directories: `app/`, `tests/`, `docker/`, `sample_data/`, `docs/`.
- Added `README.md`, `.env.example`, `requirements.txt`, and `docker-compose.yml`.
- Added a minimal FastAPI application in `app/main.py` exposing `/` and returning a Hello World message.
- Added initial project documentation including `docs/project_structure.md`.
