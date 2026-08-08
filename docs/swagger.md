# Swagger Documentation

The API exposes interactive documentation generated from the OpenAPI schema produced by FastAPI.

## Access

When the application is running, the interactive documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Raw OpenAPI schema: `http://localhost:8000/openapi.json`

## Tags

Every operation is grouped under a tag so the documentation stays navigable.

| Tag | Operations |
| --- | --- |
| `health` | `GET /health` |
| `regions` | Region CRUD endpoints under `/regions` |
| `import` | `POST /import/geojson` |

Tag descriptions are provided in `app/main.py` through `FastAPI(openapi_tags=...)`.

## Examples

Request and response models carry examples so Swagger UI displays sample values and request bodies can be pre-filled.

- `app/schemas/region.py` documents `RegionCreate`, `RegionUpdate`, and `RegionResponse` with a sample polygon geometry and region name.
- `app/schemas/geojson_import.py` documents `GeoJSONUploadResponse` with a sample import report.
- `app/schemas/health.py` documents `HealthResponse` and `HealthStatus` with a successful status payload.

Examples are declared with Pydantic `Field(examples=...)` and model-level `json_schema_extra` entries. They appear as example values and example placeholders inside Swagger UI.

## Responses

Each endpoint documents its error responses in the route decorator so Swagger UI lists them alongside the success response.

| Endpoint | Documented responses |
| --- | --- |
| `POST /regions` | `422` invalid geometry |
| `GET /regions/{region_id}` | `404` region not found |
| `PUT /regions/{region_id}` | `404` region not found, `422` invalid geometry |
| `DELETE /regions/{region_id}` | `404` region not found |
| `POST /import/geojson` | `422` invalid or unsupported GeoJSON file |

## Default Responses

FastAPI adds the following automatically:

- `422` validation error on every endpoint that accepts a body or parameters.
- `404` not found for requests that do not match any route.