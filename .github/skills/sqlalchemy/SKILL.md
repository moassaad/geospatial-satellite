---
name: sqlalchemy
description: Enforces SQLAlchemy 2.0 best practices, ORM modeling, repository pattern usage, and query optimization. Apply this when writing or reviewing database models and data access logic.
---

# SQLAlchemy Best Practices & Guidelines

## Guiding Principle

**Repositories translate business intent into efficient database operations.**

- They never contain business decisions.

## SQLAlchemy 2.0 Standard

- **Modern Syntax:** Exclusively use SQLAlchemy 2.0 syntax (`select`, `Mapped`, `mapped_column`). NEVER use the legacy `session.query(Model)`.
- **Async APIs:** Assume SQLAlchemy 2.0 async APIs when the project uses asynchronous database access.

## Base Model & Timestamps

- **Reusability:** Shared columns such as `created_at` and `updated_at` should be implemented through a reusable base model or mixin. Avoid duplicating common columns.
- **Timestamps:** Always store timestamps in UTC. Use timezone-aware datetime values.

## Primary Key Policy

- Use integer auto-increment primary keys by default.
- Use UUIDs only when there is a clear architectural reason (public identifiers, distributed systems, external exposure).
- Remain consistent across the project.

## Declarative Models & Constraints

- **Defaults:** Prefer database defaults for database-generated values. Avoid duplicating default logic in both Python and SQL unless required.
- **Constraint Naming:** Define a standard naming convention for all indexes, unique constraints, and foreign keys.
- **Indexes:** Create indexes only for fields used in filtering, joins, or ordering. Avoid unnecessary indexes.

## Relationships

- Avoid bidirectional relationships unless they are actually required.
- Prefer unidirectional relationships to reduce complexity.

## Query Construction & Filtering

- **Incremental Construction:** Compose queries incrementally. Prefer chaining query modifiers over constructing large monolithic statements.
- **Filtering:** Apply filtering in the database whenever possible. Avoid filtering ORM collections in Python.
- **Spatial Integration:** Spatial queries and geometry-specific operations belong to dedicated repository methods and should rely on **PostGIS** functions rather than application-side filtering.

## Repository Rules & Returns

- **Return Types:** Repositories should return ORM models, collections of ORM models, or scalar values when appropriate. Avoid returning tuples unless explicitly required.
- **Pagination:** Repositories returning collections should support pagination parameters when appropriate.
- **Bulk Operations:** Avoid bulk operations unless explicitly requested. Favor ORM consistency over premature optimization.

## Loading Strategy & ORM Identity

- **Explicit Loading:** Choose explicitly. Never rely on implicit lazy loading.
  - Prefer `joinedload` for one-to-one / many-to-one.
  - Prefer `selectinload` for collections.
- **ORM Identity:** Reuse ORM instances already attached to the session. Avoid unnecessary database fetches for managed entities.

## Transactions & Session Lifecycle

- **Session Lifecycle:** The session lifecycle belongs to the application dependency layer. Repositories should never close sessions.
- **Transaction Boundaries:** Services own the transaction boundaries. Repositories NEVER call `session.commit()`.
- **Flushing:** Use `session.flush()` only when the generated identifier or persisted state is immediately required. Avoid unnecessary `flush()` calls.

## Migrations & Soft Deletion

- **Alembic:** All schema changes must be handled exclusively via Alembic migrations. Never use `Base.metadata.create_all()`.
- **Soft Deletion:** If soft delete is required, explicitly filter out soft-deleted records in all read queries by default.

## AI Decision Rule & Scope

- If several SQLAlchemy implementations are valid, prefer the implementation that:
  1. Minimizes queries.
  2. Minimizes ORM complexity.
  3. Avoids raw SQL (unless essential for PostGIS functions).
  4. Preserves readability.
- **Scope:** Only add the models, columns, or queries strictly required for the task. Do not rewrite unrelated repository code.

## Self Review Checklist

- [ ] SQLAlchemy 2.0 syntax applied strictly.
- [ ] Base model used for common columns (timestamps).
- [ ] UTC / Timezone-aware datetimes used.
- [ ] Queries constructed incrementally.
- [ ] Explicit loading strategies used (`joinedload` / `selectinload`).
- [ ] No `session.commit()` inside repositories.
- [ ] PostGIS functions utilized for spatial filtering.
