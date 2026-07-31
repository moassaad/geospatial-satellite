---
name: project-context
description: The single source of truth for the project. Contains the core domain, technical stack, structure, roadmap, and strict operational boundaries. Apply this to align all generated outputs with the specific scope of the Satellite Data API project.
---

# Project Context & Strategy

## Project Identity

- **Goal:** Build a RESTful API for managing and querying Regions of Interest (ROIs) for Earth Observation and satellite image cataloging.
- **Nature:** A learning-oriented portfolio project designed to demonstrate backend engineering, geospatial processing, and modern software architecture.

## Official Technology Stack

- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Database:** PostgreSQL 16 + PostGIS
- **ORM:** SQLAlchemy 2.0, GeoAlchemy2
- **Spatial Processing:** GeoPandas, Shapely
- **Validation:** Pydantic v2
- **Containerization:** Docker, Docker Compose
- **Testing:** Pytest
- **Migration:** Alembic

## Official Project Structure

```text
app/
    config/
    database/
    models/
    schemas/
    repositories/
    services/
    routers/
    utils/
tests/
sample_data/
docker/
README.md
docker-compose.yml
requirements.txt

```

- **Restriction:** Never introduce additional folders without explicit request.

## Planned API Scope

- `POST /regions`
- `GET /regions`
- `GET /regions/{id}`
- `PUT /regions/{id}`
- `DELETE /regions/{id}`
- `POST /regions/import`
- `GET /regions/intersects`
- `GET /regions/contains`
- `GET /health`
- **Forbidden:** Do not generate endpoints for `/users`, `/login`, `/auth`, or any CRUD for non-existent entities.

## Data Flow & Repository Philosophy

- **Data Flow:** GeoJSON -> GeoPandas -> Validation -> Repository -> PostGIS -> Spatial Query -> API Response
- **Philosophy:**
- **Repositories:** Persistence only.
- **Services:** Business rules.
- **PostGIS:** Spatial calculations.
- **GeoPandas:** Preprocessing.

## Definition of Done

A task is complete only if:

- Architecture is respected.
- Type hints are complete.
- PEP8 is compliant.
- No dead code or TODOs.
- No placeholder implementation.
- Docker builds correctly.
- Tests pass (if applicable).
- Documentation updated (if applicable).
- Commit ready.

## AI Operational Rules

- **Conflict Precedence:** When the requested task conflicts with this document, **this document takes precedence.**
- **Uncertainty:** If uncertainty exists, ask one clarification question. Never invent requirements.
- **Scope Control:** Implement only the requested change. Do not be creative. Do not redesign.

## Roadmap & Boundaries

- **Roadmap Phases:** Foundation -> Database -> Region Management -> GeoJSON Import -> Spatial Queries -> Deployment -> Testing & Documentation.
- **Non-Goals (Excluded):** Authentication, Authorization, User management, Frontend, Cloud deployment, Satellite image processing/downloading.
- **Future Scope (Excluded):** Raster support, Satellite metadata, Caching, Background jobs. These are intentionally excluded from the current implementation.

## Self-Review Checklist

- [ ] Does the proposed feature strictly align with the ROIs/Cataloging domain?
- [ ] Did I verify this is not in the "Non-Goals" or "Future Scope" list?
- [ ] Is the proposed implementation following the strict Project Structure?
- [ ] Did I respect the Definition of Done?
