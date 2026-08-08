---
name: testing-pytest
description: Enforces professional testing standards using Pytest. Focuses on AAA pattern, structural mirroring, integration testing with PostGIS, and deterministic behavior. Apply when writing or reviewing test suites.
---

# Testing Best Practices & Guidelines

## Guiding Principles

- **Tests describe observable behavior.** A reader should understand the system by reading the tests.
- **Deterministic Execution:** Tests must produce identical results every run. Never depend on the current time or randomness.
- **Functional Integrity:** Each test verifies exactly one behavior.

## Test Organization

- **Mirror Structure:** Test modules must mirror the application structure.
  - `app/services/user_service.py` -> `tests/unit/services/test_user_service.py`
- **Separation:** Strictly separate tests by type:
  - `tests/unit/`: Logic isolated from DB/IO.
  - `tests/integration/`: Interaction with DB, APIs, or external boundaries.
  - `tests/fixtures/`: Reusable test setups and mocks.

## Test Methodology

- **AAA Pattern (Arrange, Act, Assert):** Explicitly structure tests. Separate sections with blank lines.
- **Data Quality:** Use realistic test data (e.g., "Cairo" instead of "foo"). Avoid meaningless placeholders.
- **Parametrization:** Use `pytest.mark.parametrize` for multiple inputs that share the same behavior.
- **Independence:** Tests must be independent. Test A must not rely on state from Test B.

## Mocking & Boundaries

- **External Boundaries:** Mock only external boundaries (HTTP requests, cloud services, email providers, message brokers).
- **Pure Logic:** Do not mock pure business logic or repositories unless absolutely necessary.
- **Database:** Integration tests should use a real test database. Rollback transactions after execution to leave the DB unchanged.

## Async & FastAPI Standards

- **Async:** Use `pytest-asyncio` strictly. Do not mix sync and async test styles.
- **FastAPI:** Use `TestClient` or `AsyncClient`. Verify `status_code`, `response_schema`, and `response_body`.
- **SQLAlchemy & PostGIS:** Spatial queries must be verified using **real geometries**. Do not mock PostGIS functions. Use representative polygons and points for intersections.

## Prohibitions & Anti-Patterns

- **Forbidden:**
  - Never test private methods or internal implementation details.
  - Never assert internal state if observable behavior is sufficient.
  - Never measure execution time within functional tests (Performance != Functional).
  - Never access external live services during unit tests.

## AI Decision Rules

- Generate only tests required by the requested feature.
- Do not invent additional scenarios unless explicitly requested.

## Self Review Checklist

- [ ] Is the test deterministic (no time/random dependencies)?
- [ ] Does the test verify exactly one observable behavior?
- [ ] Does it avoid unnecessary mocks (especially for pure logic/repositories)?
- [ ] Is it readable without needing comments?
- [ ] Would the test fail if the feature broke?
- [ ] Does the test structure mirror the application structure?
- [ ] Are real geometries used for spatial predicates?
