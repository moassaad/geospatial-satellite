# AGENT.md

# Geospatial Satellite Data API

## Purpose

This repository is built incrementally using small, independent sprints.

Every sprint must leave the project in a stable, runnable state.

The objective is to build a clean, production-like codebase that demonstrates backend engineering best practices using Python, FastAPI, PostgreSQL/PostGIS, GeoPandas, Docker, and SQLAlchemy.

---

# Primary Goal

Your responsibility is to implement **only the current sprint**.

Do not implement future features.

Do not redesign previous work.

Do not perform unrelated refactoring.

---

# General Rules

Always:

- Follow the project architecture.
- Follow all installed Skills.
- Produce clean, readable code.
- Keep implementations simple.
- Prefer maintainability over clever solutions.
- Use descriptive naming.
- Keep files focused on one responsibility.
- Leave the project in a working state.

Never:

- Add features outside the current sprint.
- Rename project folders without request.
- Delete existing code unless required.
- Introduce breaking changes.
- Generate placeholder code that is never used.
- Add unnecessary abstractions.
- Over-engineer the solution.
- Generate comments unless explicitly requested.

---

# Architecture

The project follows a layered architecture.

```
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

Rules:

- Routers never contain business logic.
- Services contain business logic.
- Repositories communicate with the database.
- Models only describe database entities.
- Schemas handle request/response validation.

---

# Project Structure

```
app/
    main.py

    config/

    core/

    database/

    dependencies/

    models/

    repositories/

    routers/

    schemas/

    services/

    utils/

tests/

docker/

sample_data/

docs/
```

Do not modify this structure unless explicitly requested.

---

# Sprint Rules

Every sprint must satisfy all of the following:

1. Implement exactly one feature.
2. Keep the application runnable.
3. Update the required documentation.
4. Produce one commit only.
5. Never break previous functionality.

---

# Documentation

Whenever a sprint introduces a feature:

Update:

- README.md (only if needed)
- docs/changelog.md

Update feature documentation if applicable:

- docs/api.md
- docs/database.md
- docs/postgis.md
- docs/docker.md
- docs/testing.md
- docs/project_structure.md

Never duplicate documentation.

---

# Git Rules

One sprint = One commit.

Use Conventional Commits.

Examples:

feat(api): add region CRUD endpoints

feat(postgis): enable spatial extension

feat(import): import GeoJSON regions

docs: update project documentation

test: add region integration tests

Do not create multiple commits.

---

# Code Style

Follow:

- PEP 8
- Type hints
- Small functions
- Single Responsibility Principle
- SOLID
- Clean Code

Avoid:

- Long functions
- Deep nesting
- Duplicate code
- Magic values
- Wildcard imports

---

# FastAPI Rules

- Use APIRouter.
- Use dependency injection.
- Use response_model.
- Validate requests with Pydantic.
- Never access the database directly from routers.

---

# SQLAlchemy Rules

- Use ORM.
- Use Declarative Models.
- Avoid raw SQL unless required for PostGIS.
- Keep sessions properly managed.

---

# PostGIS Rules

Use PostGIS functions whenever spatial operations are required.

Examples:

- ST_Contains
- ST_Intersects
- ST_DWithin

Do not reimplement spatial algorithms in Python.

---

# GeoPandas Rules

Use GeoPandas only for:

- Reading GeoJSON
- Reading Shapefiles
- CRS transformation
- Geometry validation

Business logic must remain inside services.

---

# Docker Rules

- Keep Docker images minimal.
- Use environment variables.
- Never hardcode secrets.
- Use Docker Compose for local development.

---

# Testing

When the sprint affects business logic:

- Add or update tests.

Prefer pytest.

---

# Definition of Done

A sprint is complete only if:

- Feature implemented.
- Application runs.
- Documentation updated.
- Tests pass (if applicable).
- No linting issues.
- No breaking changes.
- One commit message suggested.

---

# Expected Output

At the end of every sprint provide:

## Files Changed

List all modified files.

## Summary

Explain what was implemented.

## Documentation Updated

List updated documentation files.

## Verification

Explain how to verify the feature.

## Suggested Commit

Provide exactly one Conventional Commit message.

Do not perform the commit.

---

# Decision Making

When multiple implementations are possible:

Choose the solution that is:

1. Simpler
2. More readable
3. Easier to maintain
4. More aligned with FastAPI best practices

Never choose complexity unless explicitly requested.

---

# Important

The goal of this repository is educational while maintaining production-quality standards.

Favor clarity over cleverness.

Keep the codebase understandable for junior and mid-level backend developers.

---

# Environment

Assume the development environment is already configured.

Do not:
- create virtual environments
- activate virtual environments
- install Python
- install system packages

Only update requirements.txt when new Python dependencies are introduced.

---

# Dependency Management

If a sprint introduces a new Python package:
- Add it to requirements.txt.
- Do not install it.

---

# Container Management

Do not run Docker commands.

Only update:
- Dockerfile
- docker-compose.yml

---

# Assumptions

Assume:

- Git is initialized.
- Python is installed.
- Docker and Docker Compose are installed.
- PostgreSQL can run inside Docker.
- A virtual environment already exists.
- The project dependencies are installed.

Do not perform environment setup unless explicitly requested.

---

# Constraints:
- Do not modify unrelated files.
- Do not implement future sprints.
- Keep the application runnable.
- Follow AGENT.md.
- Follow PROJECT_CONTEXT.md.
- Use installed Skills.

