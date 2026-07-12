# Docker Environment

The application is containerized with Docker Compose. The stack includes the FastAPI application and a PostgreSQL/PostGIS database.

## Services

### `app`

- Built from the project `Dockerfile`.
- Runs the FastAPI application with Uvicorn.
- Exposes port `8000`.
- Loads environment variables from `.env`.
- Overrides `DATABASE_URL` internally to connect to the `db` service by name.
- Waits for the `db` service health check to pass before starting.

### `db`

- Uses the official `postgis/postgis:16-3.4` image.
- Exposes port `5432`.
- Persists data in the `postgres_data` Docker volume.
- Includes a readiness health check via `pg_isready`.

## Network

Both services are attached to the dedicated bridge network `satellite_network`. The application resolves the database via the Compose service name `db`, so hardcoded container names are not required for communication.

## Volumes

- `postgres_data`: persistent storage for PostgreSQL data.

## Usage

Build and start all services:

```bash
docker compose up --build -d
```

After the containers are healthy, verify the root endpoint:

```bash
curl http://localhost:8000
```

Stop and remove the containers:

```bash
docker compose down
```

To also remove the database volume, run:

```bash
docker compose down -v
```
