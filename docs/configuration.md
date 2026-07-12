# Configuration

Application configuration is managed with Pydantic Settings and loaded from environment variables. A `.env` file in the project root provides the values for local development.

## Required Variables

- `APP_NAME`: Human-readable name of the application used in the FastAPI metadata.
- `DATABASE_URL`: SQLAlchemy-compatible connection string for the PostgreSQL database.

## Optional Variables

These values are used by the `docker-compose.yml` database service:

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

## Example `.env`

```bash
APP_NAME=Geospatial Satellite Data API
DATABASE_URL=postgresql+psycopg2://satellite_user:satellite_password@localhost:5432/satellite_db
POSTGRES_USER=satellite_user
POSTGRES_PASSWORD=satellite_password
POSTGRES_DB=satellite_db
```

## Accessing Settings

Import the `Settings` instance where configuration is needed:

```python
from app.config.settings import Settings

settings = Settings()
```

The instance reads the `.env` file once and exposes the validated values as attributes.
