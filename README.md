# Geospatial Satellite Data API

A clean, maintainable, and production-like RESTful API for managing and querying Regions of Interest (ROIs) used in Earth Observation and satellite image cataloging.

The application stores geographic regions in PostgreSQL/PostGIS, accepts GeoJSON imports, runs spatial queries directly in the database, and exposes the whole catalog through a REST API with interactive OpenAPI documentation.

## Features

- Region CRUD: create, list, read, update, and delete regions.
- GeoJSON import through a file upload endpoint, parsed with GeoPandas.
- Spatial queries executed in PostGIS:
  - `ST_Contains` — find regions containing a point.
  - `ST_Intersects` — find regions intersecting a point.
- Persistence in PostGIS with geometries standardized to `EPSG:4326`.
- Interactive API documentation (Swagger UI, ReDoc, OpenAPI schema).
- Health check endpoint that reports database connectivity.
- Docker Compose stack for the application and the database.

## Architecture

The project follows a layered architecture. Each layer has a single responsibility and points only downward:

```
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

- **Routers** handle HTTP requests, validation, and error mapping. They contain no business logic.
- **Services** implement business rules and coordinate repositories.
- **Repositories** encapsulate all persistence logic and talk to the database.
- **Models** describe database entities.
- **Schemas** validate request payloads and serialize responses.

Business logic lives only in services. Routers stay thin and delegate to the service layer.

## Tech Stack

- **Programming Language:** Python 3.12+
- **Framework:** FastAPI
- **Database:** PostgreSQL 16
- **Spatial Extension:** PostGIS
- **ORM:** SQLAlchemy 2.0 with GeoAlchemy2
- **Geospatial Processing:** GeoPandas, Shapely
- **Validation:** Pydantic v2
- **Migrations:** Alembic
- **Containerization:** Docker, Docker Compose
- **Testing:** pytest

## Project Structure

```
app/
    main.py
    config/
    core/
    database/
    models/
    repositories/
    routers/
    schemas/
    services/
    utils/

tests/
    integration/

alembic/
docker/
docs/

README.md
.env.example
requirements.txt
docker-compose.yml
```

Each folder has one responsibility:

- `app/routers/` — HTTP endpoints (thin).
- `app/services/` — business logic.
- `app/repositories/` — database access.
- `app/models/` — ORM entities.
- `app/schemas/` — request/response validation.
- `app/database/` — engine, session, and ORM base.
- `tests/integration/` — full-stack tests against a real PostGIS database.

## Installation

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (for the database and the full stack)
- PostgreSQL with PostGIS (when running without Docker)

### 1. Clone and prepare the environment

```bash
git clone https://github.com/moassaad/geospatial-satellite.git
cd geospatial-satellite
python3 -m venv .venv
```

Activate the virtual environment:

- **Windows**
  ```bash
  .venv\Scripts\activate
  ```
- **Linux / macOS**
  ```bash
  source .venv/bin/activate
  ```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the example file and adjust values if needed:

```bash
cp .env.example .env
```

See [Configuration](docs/configuration.md) for the full list of variables.

## Configuration

The application is configured through environment variables read by Pydantic Settings from `.env`.

| Variable | Required | Description |
| --- | --- | --- |
| `APP_NAME` | Yes | Name used as the FastAPI application title. |
| `DATABASE_URL` | Yes | SQLAlchemy connection string for PostgreSQL. |
| `POSTGRES_USER` | No | Database user used by the Compose `db` service. |
| `POSTGRES_PASSWORD` | No | Database password used by the Compose `db` service. |
| `POSTGRES_DB` | No | Database name used by the Compose `db` service. |

Example:

```bash
APP_NAME=Geospatial Satellite Data API
DATABASE_URL=postgresql+psycopg2://satellite_user:satellite_password@localhost:5433/satellite_db
POSTGRES_USER=satellite_user
POSTGRES_PASSWORD=satellite_password
POSTGRES_DB=satellite_db
```

## Running the Application

### With Docker Compose (recommended)

```bash
docker compose up --build -d
```

The full stack starts: the FastAPI application on port `8000` and PostgreSQL/PostGIS on port `5433`.

Verify the root endpoint:

```bash
curl http://localhost:8000
```

### Without Docker

1. Make sure PostgreSQL and PostGIS are running and reachable at `DATABASE_URL`.
2. Apply the database migrations:

   ```bash
   alembic upgrade head
   ```

3. Start the API:

   ```bash
   uvicorn app.main:app --reload
   ```

## API

When the application is running, the interactive documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI schema: `http://localhost:8000/openapi.json`

### Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Hello World root message. |
| `GET` | `/health` | Application and database health status. |
| `POST` | `/regions` | Create a region. |
| `GET` | `/regions` | List all regions. |
| `GET` | `/regions/{region_id}` | Get a region by ID. |
| `PUT` | `/regions/{region_id}` | Update a region. |
| `DELETE` | `/regions/{region_id}` | Delete a region. |
| `POST` | `/contains` | Find regions containing a point. |
| `POST` | `/intersects` | Find regions intersecting a point. |
| `POST` | `/import/geojson` | Import a GeoJSON file. |

## Examples

### Create a region

```bash
curl -X POST http://localhost:8000/regions \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cairo",
    "geometry": {
      "type": "Polygon",
      "coordinates": [
        [[31.0, 30.0], [31.5, 30.0], [31.5, 30.5], [31.0, 30.5], [31.0, 30.0]]
      ]
    }
  }'
```

Response (`201 Created`):

```json
{
  "id": 1,
  "name": "Cairo",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [[31.0, 30.0], [31.5, 30.0], [31.5, 30.5], [31.0, 30.5], [31.0, 30.0]]
    ]
  },
  "created_at": "2026-07-19T21:15:00.123456Z"
}
```

### List regions

```bash
curl http://localhost:8000/regions
```

### Spatial queries

Find the region containing a point inside Cairo:

```bash
curl -X POST http://localhost:8000/contains \
  -H "Content-Type: application/json" \
  -d '{"latitude": 30.2, "longitude": 31.2}'
```

Find the region intersecting the same point:

```bash
curl -X POST http://localhost:8000/intersects \
  -H "Content-Type: application/json" \
  -d '{"latitude": 30.2, "longitude": 31.2}'
```

Both return an array of matching regions, or an empty array when no region matches.

### Import a GeoJSON file

```bash
curl -X POST http://localhost:8000/import/geojson \
  -F file=@regions.geojson
```

### Health check

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "ok",
  "database": {
    "status": "ok"
  }
}
```

### Status codes

| Status | Meaning |
| --- | --- |
| `200 OK` | Successful read or update. |
| `201 Created` | Successful creation or import. |
| `204 No Content` | Successful deletion. |
| `404 Not Found` | Region does not exist. |
| `422 Unprocessable Entity` | Invalid geometry or unsupported GeoJSON file. |

## Spatial data

Geometries are stored and processed with PostGIS using `EPSG:4326`.

- **Geometry types:** `Polygon` and `MultiPolygon`.
- **Coordinate order:** GeoJSON stores longitude first, then latitude (`[lon, lat]`).
- **Spatial queries** use `ST_GeomFromText`, `ST_Contains`, and `ST_Intersects` directly in the database, backed by a GiST index on the geometry column.
- Imported files are parsed with GeoPandas, transformed to `EPSG:4326`, and validated before persistence.

## Testing

The test suite is split into unit tests and integration tests. See [docs/testing.md](docs/testing.md) for details.

Run the full suite:

```bash
pytest
```

Integration tests require a reachable PostGIS database and are skipped automatically when one is not available.

## Docker

The project includes a `Dockerfile` and a Compose stack with an `app` service and a PostGIS `db` service. See [docs/docker.md](docs/docker.md) for the full breakdown.

```bash
docker compose up --build -d
```

## Screenshots

The project ships with interactive API documentation that demonstrates every endpoint with examples:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

After starting the stack, open `http://localhost:8000/docs` to interact with the API and explore the region CRUD, spatial queries, and GeoJSON import endpoints directly from the browser.

## Roadmap

The following features are intentionally postponed and are not implemented:

- JWT authentication and role-based access control.
- Pagination and filtering.
- Logging, metrics, and rate limiting.
- Satellite image processing and raster support.
- Cloud deployment and CI/CD pipelines.

## License

This project is intended for educational and portfolio use.