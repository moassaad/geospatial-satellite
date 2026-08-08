# Testing

The project uses pytest. Tests are split into unit tests and integration tests.

## Running Tests

```bash
pytest
```

Run only the unit tests:

```bash
pytest tests --ignore=tests/integration
```

Run only the integration tests:

```bash
pytest tests/integration
```

## Unit Tests

Unit tests live directly under `tests/` and mock the database layer, so they run without a database.

- `tests/test_geojson_import.py`
- `tests/test_spatial.py`

They verify:

- GeoJSON import validation and parsing.
- Spatial service delegation and PostGIS function usage.

## Integration Tests

Integration tests live under `tests/integration/` and exercise the full stack against a real PostGIS database through the FastAPI `TestClient`.

They cover:

- CRUD operations on `/regions`
- Health check on `/health`
- Containment query on `/contains`
- Intersection query on `/intersects`

The fixture in `tests/integration/conftest.py`:

- Connects to a test database.
- Creates the schema if it does not exist.
- Wraps every test in a transaction that is always rolled back, leaving the database unchanged.
- Skips the suite when the test database is unreachable.

### Test Database Configuration

The integration tests use the `TEST_DATABASE_URL` environment variable when it is set, and fall back to `DATABASE_URL` (from `.env`) otherwise. When using Docker Compose, the integration tests can run against the configured `satellite_db`.

Example:

```bash
export TEST_DATABASE_URL=postgresql+psycopg2://satellite_user:satellite_password@localhost:5432/satellite_db
pytest tests/integration
```

## Running with Docker Compose

1. Start the stack:

   ```bash
   docker compose up -d db
   ```

2. Run the full suite:

   ```bash
   pytest
   ```

The integration tests connect to the database exposed on `localhost:5432`.