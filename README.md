# Geospatial Satellite Data API

A clean, maintainable, and production-like RESTful API for managing and querying Regions of Interest (ROIs) used in Earth Observation and satellite image cataloging.

## Tech Stack

- Python 3.12+
- FastAPI
- PostgreSQL 16
- PostGIS
- SQLAlchemy 2.0
- GeoPandas
- Docker & Docker Compose

## Project Structure

See [docs/project_structure.md](docs/project_structure.md).

## Getting Started

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application locally with Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

3. Visit `http://localhost:8000` to verify the root endpoint.

## Docker Compose

Start the PostgreSQL/PostGIS database service:

```bash
docker compose up db -d
```

## License

This project is intended for educational and portfolio use.
