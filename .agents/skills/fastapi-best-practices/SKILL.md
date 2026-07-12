---
name: fastapi-best-practices
description: Enforces FastAPI best practices, including routing, dependency injection, validation, and serialization. Apply this when creating, modifying, or reviewing FastAPI endpoints.
---

# FastAPI Best Practices & Guidelines

## Guiding Principle

**FastAPI should remain a thin HTTP layer.**

- Business logic belongs to services.
- Persistence belongs to repositories.

## Router Organization & Responsibilities

- **Organization:** Each resource should have its own router module. Register routers from a central router registry. Avoid placing unrelated endpoints in the same router.
- **Strict Flow:** Routers should ONLY:
  1. Validate input.
  2. Resolve dependencies.
  3. Call one service.
  4. Return one response.
  - **Nothing more.**
- **Large Endpoints:** If an endpoint grows significantly, move the logic to services. Never expand the router.

## HTTP Method Usage

- `GET`: Read only.
- `POST`: Create resources or execute non-idempotent actions.
- `PUT`: Replace a resource.
- `PATCH`: Partial update.
- `DELETE`: Remove a resource.

## Validation & Serialization (Pydantic)

- **Validation:** Validate as early as possible. Prefer declarative validation through Pydantic. Avoid manual validation inside routers.
- **Response Models:** Always explicitly define `response_model` in the route decorator.
- **Serialization:** Never return dictionaries when a response model exists. Always let FastAPI serialize Pydantic models. Avoid manual dict construction and avoid `.model_dump()` unless transformation is explicitly required.

## API Response Consistency & Status Codes

- **Consistency:** Responses should follow a consistent structure across the project. Avoid returning different JSON shapes for similar operations. Return only the fields defined by the response schema.
- **Explicit Status Codes:** Always define `status_code` (e.g., `201 Created` for POST, `204 No Content` for DELETE without body, `200 OK` default).

## Dependency Injection (`Depends`)

- **Composition:** Dependencies should be composable. Avoid nested dependency chains unless necessary. Prefer explicit dependencies.
- **Database Sessions:** Database sessions MUST be injected. Never create database sessions inside routers.
- **Authentication:** Authentication should be implemented through dependencies. Never perform authentication logic directly inside endpoints.

## Exception Handling

- **Domain Mapping:** Domain exceptions should be mapped consistently to HTTP exceptions. Do not translate the same domain exception differently across endpoints.
- **No Internal Leaks:** Never expose raw database errors or stack traces to the client. Let FastAPI handle `RequestValidationError` automatically.

## Advanced Request Handling

- **File Uploads:** Validate file type before processing. Stream files when possible. Avoid loading unnecessarily large files into memory (critical for spatial data).
- **Pagination:** Endpoints returning collections should support pagination when appropriate.
- **Background Tasks:** Use `BackgroundTasks` only for lightweight post-response operations. Do not use them for long-running jobs.
- **Streaming:** Use `StreamingResponse` only when returning large datasets or files.

## Health Check & Lifespan

- **Health Endpoint:** Provide one lightweight health endpoint. Avoid embedding business logic inside health checks.
- **Lifespan:** Use `asynccontextmanager` for app initialization. Do NOT use deprecated `@app.on_event`.

## OpenAPI Documentation

- Keep OpenAPI documentation concise.
- Avoid documenting obvious behavior.
- Document only business-specific behavior.

## AI Scope & Decision Rules

When generating or modifying FastAPI code:

- **Decision Rule:** If multiple FastAPI implementations are valid, choose the implementation that: uses fewer dependencies, follows FastAPI conventions, minimizes code, and improves readability.
- **No Custom Wrappers:** Do not create custom decorators to wrap FastAPI's built-in routing or dependency injection.
- **Minimal Scope:** Only add the endpoints requested. Do not add full CRUD if only one endpoint was requested.

## Self Review Checklist

Before finishing, verify:

- [ ] Router strictly follows the Validate -> Resolve -> Call -> Return flow.
- [ ] Explicit `response_model` and `status_code` are defined.
- [ ] No ORM models or dictionaries are returned directly.
- [ ] DB sessions and Authentication are injected via `Depends()`.
- [ ] Exceptions are mapped consistently.
- [ ] No business logic leaked into the router.
