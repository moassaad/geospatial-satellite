# Changelog

## Sprint 18 - Swagger Improvements

- Added OpenAPI examples to request and response schemas in `app/schemas/region.py`, `app/schemas/geojson_import.py`, and `app/schemas/health.py`.
- Documented error responses in the route decorators of `app/routers/region.py` and `app/routers/geojson_import.py`.
- Added tag metadata through `openapi_tags` in `app/main.py`.
- Added `docs/swagger.md` documenting tags, examples, and documented responses.

## Sprint 17 - Intersection Query

- Added `POST /intersects` to run a spatial intersection query.
- Added `find_intersecting_regions` to `app/repositories/region_repository.py` using PostGIS `ST_Intersects`.
- Added `find_regions_intersecting_point` to `app/services/region_service.py`.
- Extended `app/routers/spatial.py` with the new intersection endpoint.
- Added `tests/test_spatial.py` to cover the new spatial behavior.
- Updated `docs/spatial-query.md` with the intersection query documentation.

## Sprint 16 - Containment Query

- Added `POST /contains` to run a spatial containment query.
- Added `PointRequest` schema with `latitude` and `longitude`.
- Added `find_containing_regions` to `app/repositories/region_repository.py` using PostGIS `ST_Contains`.
- Added `find_regions_containing_point` to `app/services/region_service.py`.
- Created `app/routers/spatial.py` and wired it into `app/main.py`.
- Added `docs/spatial-query.md` documenting the containment query.

## Sprint 15 - Persist Imported Data

- Updated `POST /import/geojson` to persist parsed regions into PostGIS.
- Changed response status from `202 Accepted` to `201 Created`.
- Added `create_many` to `app/repositories/region_repository.py` for bulk insertion.
- Updated `app/services/geojson_import_service.py` to build `RegionCreate` objects and persist via repository.
- Extended `app/schemas/geojson_import.py` with `imported_ids` field.
- Changed model geometry column to `Geometry(srid=4326)` to support both Polygon and MultiPolygon.
- Added Alembic migration `alter_region_geometry_type` to alter column type and add GIST spatial index.
- Updated `docs/import.md` with new response and status code.

## Sprint 14 - GeoPandas Parser

- Integrated GeoPandas parsing into the `POST /import/geojson` endpoint.
- Added `geopandas` to `requirements.txt`.
- Updated `app/services/geojson_import_service.py` to parse uploaded GeoJSON with GeoPandas, validate CRS, transform to EPSG:4326, and enforce Polygon/MultiPolygon geometry types.
- Extended `app/schemas/geojson_import.py` with `feature_count`, `columns`, and `crs` fields.
- Updated `docs/import.md` with parsed response metadata and geometry constraints.

## Sprint 13 - GeoJSON Upload Endpoint

- Added `POST /import/geojson` endpoint accepting GeoJSON file uploads.
- Created `app/routers/geojson_import.py`, `app/services/geojson_import_service.py`, and `app/schemas/geojson_import.py`.
- Added `InvalidGeoJSONFileError` to `app/core/exceptions.py` for file validation errors.
- Added `python-multipart` to `requirements.txt` for multipart form-data support.
- Wired the import router into `app/main.py`.
- Added `docs/import.md` documenting the import endpoint.

## Sprint 12 - Region Update API

- Added `PUT /regions/{region_id}` and `DELETE /regions/{region_id}` to `app/routers/region.py`.
- Mapped `RegionNotFoundError` and `InvalidGeometryError` to the appropriate HTTP status codes in the new endpoints.
- Updated `docs/api.md` with PUT and DELETE documentation and status codes.

## Sprint 11 - Region Read API

- Created `app/routers/region.py` with `POST /regions`, `GET /regions`, and `GET /regions/{region_id}`.
- Updated `RegionResponse` to serialize PostGIS geometry as GeoJSON.
- Mapped `RegionNotFoundError` to `404 Not Found` and `InvalidGeometryError` to `422 Unprocessable Entity`.
- Wired the region router into `app/main.py`.
- Added `docs/api.md` documenting the available endpoints and status codes.

## Sprint 10 - Region Service

- Created `app/services/region_service.py` implementing region business logic.
- Added `app/core/exceptions.py` with `RegionNotFoundError` and `InvalidGeometryError`.
- Added geometry validation in the service using Shapely before delegating to the repository.
- Added `docs/services.md` documenting the region service and domain exceptions.

## Sprint 09 - Region Repository

- Added `shapely` to `requirements.txt`.
- Created `app/repositories/region_repository.py` with CRUD operations for the `Region` model.
- Converted GeoJSON geometry dictionaries to GeoAlchemy2 geometry objects in the repository.
- Added `docs/repositories.md` documenting the region repository and its responsibilities.

## Sprint 07 - Region Database Model

- Added `geoalchemy2` to `requirements.txt`.
- Created `app/models/region.py` with `id`, `name`, `geometry`, and `created_at` fields.
- Updated `alembic/env.py` to import the `Region` model so it is registered in `Base.metadata`.
- Added `docs/domain-model.md` documenting the `Region` entity.

## Sprint 06 - Health Check

- Added `/health` endpoint.
- Created `app/routers/health.py`, `app/services/health_service.py`, and `app/repositories/health_repository.py`.
- Added `app/schemas/health.py` for the health response model.
- Wired the health router into `app/main.py`.
- Added `docs/health.md` documenting the endpoint and architecture.

## Sprint 05 - PostGIS Support

- Added `docker/initdb/01_init_postgis.sql` to create the PostGIS extension.
- Updated `docker-compose.yml` to mount the init script into `/docker-entrypoint-initdb.d/`.
- Added `docs/postgis.md` explaining PostGIS initialization and verification.

## Sprint 04 - Alembic Migrations

- Added `alembic` to `requirements.txt`.
- Created `alembic.ini` and the `alembic/` directory with `env.py`, `script.py.mako`, and `versions/`.
- Configured `alembic/env.py` to read `DATABASE_URL` from Pydantic Settings and use `Base.metadata`.
- Added `docs/migrations.md` with Alembic usage instructions.

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
