# Changelog

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
