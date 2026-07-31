---
name: docker
description: Enforces Docker best practices, efficient builds, modern docker-compose setups, and secure configurations. Apply when writing or modifying Dockerfiles, docker-compose.yml, or container scripts.
---

# Docker & Containerization Guidelines

## Guiding Principles

- **Containers package applications. They should not replace application architecture.**
- Containers must be ephemeral, minimal, and secure.
- Fail fast: Build processes and runtimes should fail immediately if a dependency or required environment variable is missing.

## Dockerfile Fundamentals

- **Version Pinning:** Pin base image versions explicitly. Avoid using floating tags such as `latest` (e.g., use `python:3.12-slim`).
- **Base Images:** Avoid `alpine` for Python applications unless explicitly requested. Use `-slim` variants to prevent issues with C-extensions (like GeoPandas/Shapely).
- **Working Directory:** Always define a `WORKDIR`. Avoid relying on the default working directory.
- **ENTRYPOINT vs CMD:** Use `CMD` for the default application command. Use `ENTRYPOINT` only when the container should always execute the same executable.

## Build Context & Layer Caching

- **Build Context:** Keep the build context as small as possible. Avoid copying unnecessary files into the image. Always use a comprehensive `.dockerignore`.
- **COPY Rule:** Copy only the files required by the application. Avoid `COPY . .` unless appropriate. Copy dependency files and install them BEFORE copying application code to maximize layer caching.
- **Image Layers:** Combine related `RUN` instructions when appropriate to reduce image layers. Do not sacrifice readability for minimal layer count.
- **Package Installation:** Install only required system packages. Avoid recommended packages when unnecessary (e.g., `--no-install-recommends`).
- **Multi-stage Builds:** Use multi-stage builds when they provide a meaningful reduction in image size or remove unnecessary build dependencies.

## Security, Execution & Logging

- **Non-Root User:** Never run the application as the `root` user.
- **Logs:** Containers should write logs to `stdout/stderr`. Avoid writing application logs to files inside the container.
- **Environment Variables:** Never hardcode secrets. Pass them at runtime. Fail fast when required environment variables are missing.

## Modern docker-compose Configuration

- **Specification:** Use the modern Compose Specification. Avoid deprecated Compose `version:` declarations at the top of the file.
- **Service Communication:** Avoid relying on container names for service communication. Services should communicate using Docker Compose service names.
- **Compose Profiles:** Use Compose profiles when development-only services should be optional.
- **Networks:** Use explicit Docker networks when multiple services communicate. Avoid exposing internal services unnecessarily.
- **Volumes:** Persist only required data. Avoid mounting unnecessary host directories.

## Health Checks & Database Initialization

- **Health Checks:** Health checks should verify application readiness, not only process existence.
- **Separation of Concerns:** Application containers should not perform database initialization. Database schema and extensions should be managed through migrations or dedicated initialization scripts.
- **PostGIS Initialization:** Database initialization scripts should be mounted through the official PostgreSQL initialization mechanism (e.g., `/docker-entrypoint-initdb.d/`). Avoid embedding initialization logic into the application container.

## AI Decision Rules

If multiple Docker implementations are valid, prefer the implementation that:

1. Is reproducible.
2. Minimizes rebuild time.
3. Minimizes image size.
4. Keeps runtime configuration external.

## Self Review Checklist

- [ ] Base image pinned explicitly (no `latest`).
- [ ] No `version:` key in `docker-compose.yml`.
- [ ] Application does not initialize the PostGIS extension.
- [ ] Build context is minimized and `COPY` instructions are strategic.
- [ ] Logs output to stdout/stderr.
- [ ] Application runs securely as a non-root user.
