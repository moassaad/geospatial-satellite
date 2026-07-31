---
name: project-architecture
description: Enforces strict adherence to the project's layered architecture, responsibilities, and coding constraints. Apply this when generating, structuring, or reviewing code to prevent architectural violations and overengineering.
---

# Project Architecture Guidelines

## Architecture Pattern

- This project follows a strict **Layered Architecture**.
- The objective is simplicity, readability, and maintainability.
- **CRITICAL:** Do NOT introduce Clean Architecture, Hexagonal Architecture, CQRS, Event Sourcing, Mediator, or other architectural patterns unless explicitly requested.

## Complexity Budget

When solving a problem, strictly follow this progression. Only move to the next level if absolutely necessary:
Simple solution → Small abstraction → Reusable code → Complex abstraction

## Dependency Direction

Dependencies only point downward. Reverse dependencies are strictly forbidden.
routers/ → services/ → repositories/ → models/

## Strict Folder & Layer Responsibilities

### routers/

- **Purpose:** Only orchestration. Receive request → Validate → Call service → Return response.
- **Rules:** Routers should remain extremely thin.
- **Forbidden:** Business logic, SQL, calculations, loops over domain objects.

### services/

- **Purpose:** Core business logic and orchestration. Services contain all business decisions and coordinate multiple repositories when needed.
- **Rules:** Services own transaction boundaries. Services never know how data is stored.
- **Forbidden:** SQL, ORM queries, HTTP objects, FastAPI imports, Request/Response models, database session management.

### repositories/

- **Purpose:** Only persistence logic. Expose intent-revealing methods (e.g., `find_by_id`, `save`).
- **Rules:** Repositories return domain objects/models. They must remain deterministic.
- **Forbidden:** Repositories NEVER commit transactions. No validation, no business rules, no response formatting, no HTTP responses.

### models/

- **Purpose:** ORM mapping only.
- **Rules:** Models should remain anemic.
- **Forbidden:** No methods except lightweight computed properties if explicitly requested. Business logic belongs to services.

### schemas/

- **Purpose:** Input validation and Output serialization using Pydantic models only.
- **Forbidden:** Business logic, ORM queries, Database access.

### database/

- **Purpose:** Engine, Session, Base, Connection configuration.
- **Forbidden:** Business logic, Repositories, API code.

### config/

- **Purpose:** Settings, Environment handling, Configuration.
- **Forbidden:** Business logic, Database queries, API code.

### utils/

- **Purpose:** Pure helper functions and stateless utilities only.
- **Forbidden:** Business logic, Database access, Network calls, Repositories.

## Forbidden Practices

- Never access the database from routers.
- Never place business logic inside repositories.
- Never duplicate logic across services.
- Never bypass the service layer (e.g., Router calling Repository directly is forbidden).
- Never create utility functions that belong to services.
- Never introduce unnecessary abstractions.

## Data Transfer & DTO Policy

- **CRITICAL:** Never expose ORM models directly to clients.
- Always expose Pydantic schemas.

## Async Policy

- Use `async` consistently.
- Do not mix sync and async unless absolutely required.
- Never block the event loop.

## Coding & Style Constraints

- **Constants:** Avoid magic strings and magic numbers. Centralize constants.
- **Logging:** Business logic never prints. Use logging. Never leave `print()` statements.
- **Naming:** Classes → `PascalCase` | Functions & Variables → `snake_case` | Constants → `UPPER_CASE`.
- **Imports:** Never use wildcard imports. Remove unused imports. Group imports according to PEP8.

## File Organization & Sizing Constraints

- **Organization:** One entity per model file, one router per resource, one service per domain, one repository per aggregate.
- **Size Limits (Strict Guidelines):** Maximum file size: 300 lines. Maximum class size: 300 lines. Maximum function size: 40 lines.
- **Function Design:** Prefer small focused functions. Prefer early returns. Avoid nested conditions. Avoid duplicated code.

## Error Handling

- **Routers:** Translate exceptions into HTTP responses.
- **Services:** Raise domain-specific exceptions.
- **Repositories:** Raise persistence exceptions only when strictly necessary.

## Dependency Injection & Configuration

- **Injection:** Dependencies must be injected. Avoid creating dependencies inside services. Avoid global state.
- **Configuration:** Configuration must come from `config/settings.py`. Never hardcode environment values. Never read environment variables outside the config layer.

## Architecture Decision Priority

When multiple valid implementations exist, prefer:

1. Existing project conventions
2. Simplicity
3. Readability
4. Maintainability
5. Performance optimization (only when required)

## AI Scope & Implementation Rules

When generating code, act as a precision tool:

- Respect the existing architecture.
- Modify ONLY requested files.
- **Scope Control:** Implement only the requested task. Avoid anticipating future requirements. Avoid premature optimization. Avoid implementing optional features.
- **Patching:** Never regenerate entire files for small changes. Patch existing code whenever possible.
- **Formatting:** Avoid unnecessary formatting changes. Do not reorder imports unless modified.
- Do NOT move, rename, or reorganize files and folders.
- Do NOT introduce additional abstractions or interfaces.
- Do NOT create helper classes unless requested.
- When ambiguous: Do not guess. Ask for clarification. Do not invent missing requirements.

## AI Decision Rules

If multiple implementations are technically correct:

Choose the implementation that:

- modifies fewer files
- introduces fewer abstractions
- follows existing project conventions
- minimizes code size
- minimizes dependencies

## Guiding Principle

When in doubt,

prefer the simplest implementation that fully satisfies the current requirement while preserving the existing architecture.

## Self Review Checklist

Before returning the final output, verify:

- [ ] Architecture respected
- [ ] Layer respected
- [ ] Imports clean & valid
- [ ] No duplicated logic
- [ ] Type hints preserved/added
- [ ] Small functions maintained
- [ ] No dead code
- [ ] No unused imports
- [ ] No TODOs or placeholder code
- [ ] No commented code
- [ ] Existing style preserved
