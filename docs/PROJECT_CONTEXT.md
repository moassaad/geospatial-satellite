# PROJECT_CONTEXT.md

# Geospatial Satellite Data API

## Project Vision

Build a clean, maintainable, and production-like RESTful API for managing and querying Regions of Interest (ROIs) used in Earth Observation and satellite image cataloging.

The project is intended to demonstrate backend engineering skills, geospatial data handling, and modern software development practices.

This repository serves as both a learning project and a professional portfolio project.

---

# Objectives

The project should demonstrate practical experience with:

- Python
- FastAPI
- PostgreSQL
- PostGIS
- GeoPandas
- SQLAlchemy
- Docker
- REST API Design
- Clean Architecture
- Git Workflow
- API Documentation

---

# Target Audience

This project is designed for:

- Backend Developers
- GIS Developers
- Technical Recruiters
- Interviewers
- Egyptian Space Agency (EgSA)
- Earth Observation Software Teams

---

# Project Scope

The application manages geographic Regions of Interest (ROIs).

Users can:

- Create regions
- Read regions
- Update regions
- Delete regions
- Import GeoJSON files
- Store geometries inside PostGIS
- Execute spatial queries
- Check whether a coordinate belongs to a region

---

# Out of Scope

The following features are intentionally excluded.

Do not implement them unless explicitly requested.

- Authentication
- Authorization
- User Management
- Satellite Image Processing
- Raster Analysis
- Image Upload
- Cloud Deployment
- Background Workers
- Message Queues
- Caching
- Frontend
- Admin Dashboard
- CI/CD Pipelines
- Monitoring
- Kubernetes
- Microservices

The project must remain focused on geospatial backend APIs.

---

# Functional Requirements

The system must support:

## Region Management

- Create Region
- List Regions
- Get Region
- Update Region
- Delete Region

---

## GeoJSON Import

The API accepts a GeoJSON file.

The application should:

- Read the file using GeoPandas
- Validate geometries
- Convert CRS when necessary
- Store data inside PostGIS

---

## Spatial Queries

Support spatial operations including:

- ST_Contains
- ST_Intersects

Example:

Input:

Latitude

Longitude

Output:

The region containing that point.

---

# Non-Functional Requirements

The application must:

- Follow Clean Code principles
- Follow SOLID principles
- Be modular
- Be maintainable
- Be testable
- Be Dockerized
- Use environment variables
- Produce OpenAPI documentation
- Be easy to understand

---

# Technical Stack

## Language

Python

---

## Framework

FastAPI

---

## Database

PostgreSQL

---

## Spatial Extension

PostGIS

---

## ORM

SQLAlchemy

---

## Validation

Pydantic

---

## Geospatial Library

GeoPandas

---

## Documentation

Swagger UI

OpenAPI

---

## Containerization

Docker

Docker Compose

---

## Testing

pytest

---

# Architecture

The application follows a layered architecture.

```
Client

↓

Router

↓

Service

↓

Repository

↓

Database
```

Business logic belongs only inside Services.

Repositories communicate only with the database.

Routers remain thin.

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

---

# Design Principles

The project prioritizes:

- Readability
- Simplicity
- Maintainability
- Explicit code
- Small modules
- Separation of concerns

Avoid unnecessary abstraction.

Avoid premature optimization.

---

# Development Strategy

Development is incremental.

Each Sprint:

- Implements one feature
- Leaves the project runnable
- Updates documentation
- Produces one commit
- Never introduces breaking changes

---

# Documentation Strategy

Documentation is part of development.

Each Sprint updates:

- docs/changelog.md

When applicable:

- docs/api.md
- docs/database.md
- docs/postgis.md
- docs/docker.md
- docs/testing.md
- docs/project_structure.md

README.md should reflect the latest stable state.

---

# Sample Dataset

The repository contains sample geospatial data.

Directory:

```
sample_data/
```

Possible files:

- regions.geojson
- governorates.geojson
- sample_points.json

These files are used only for local testing.

---

# Git Strategy

Branches

main

↓

develop

↓

feature/<feature-name>

One Sprint = One Commit

Use Conventional Commits.

---

# Coding Philosophy

Write code that another backend developer can understand immediately.

Prefer explicit implementations.

Avoid "smart" code.

Readable code is better than shorter code.

---

# Success Criteria

The project is considered complete when it can:

- Store Regions inside PostGIS
- Import GeoJSON files
- Execute spatial queries
- Expose REST APIs
- Generate Swagger documentation
- Run completely using Docker Compose
- Pass automated tests

---

# Future Enhancements

These are intentionally postponed.

Possible future improvements:

- JWT Authentication
- Role-Based Access Control
- Alembic Migrations
- Pagination
- Filtering
- Logging
- Rate Limiting
- Health Checks
- Metrics
- Raster Support
- GDAL Integration
- Rasterio Integration
- Satellite Metadata
- Cloud Deployment

These features must not be implemented unless a future sprint explicitly requires them.

---

# Final Goal

The final repository should represent a professional backend project suitable for:

- Technical interviews
- Portfolio
- GitHub showcase
- Backend engineering demonstrations
- Earth Observation backend development