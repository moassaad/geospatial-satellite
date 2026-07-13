# Migrations

Database schema migrations are managed with [Alembic](https://alembic.sqlalchemy.org/).

## Configuration

- `alembic.ini`: Alembic configuration file at the project root.
- `alembic/env.py`: environment script that reads `DATABASE_URL` from `app.config.settings.Settings` and exposes the SQLAlchemy `Base` metadata.
- `alembic/versions/`: directory for migration scripts.

## Usage

Generate a new auto-detected migration after changing models:

```bash
alembic revision --autogenerate -m "description"
```

Apply pending migrations:

```bash
alembic upgrade head
```

Revert the most recent migration:

```bash
alembic downgrade -1
```

## Requirements

Ensure dependencies are installed before running Alembic commands:

```bash
pip install -r requirements.txt
```

Because the migration environment depends on the application settings, `.env` must be present and contain a valid `DATABASE_URL`.
