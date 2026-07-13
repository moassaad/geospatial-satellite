# Health

The `/health` endpoint reports whether the application and the database connection are healthy.

## Endpoint

```http
GET /health
```

## Response

```json
{
  "status": "ok",
  "database": {
    "status": "ok"
  }
}
```

If the database is unreachable, the response still returns HTTP `200 OK` but reports the database status as `unhealthy`:

```json
{
  "status": "ok",
  "database": {
    "status": "unhealthy"
  }
}
```

## Architecture

The endpoint follows the layered architecture:

- **Router:** `app/routers/health.py` accepts the request and injects a database session.
- **Service:** `app/services/health_service.py` builds the health response.
- **Repository:** `app/repositories/health_repository.py` executes a simple `SELECT 1` query to verify connectivity.

## Usage

```bash
curl http://localhost:8000/health
```
