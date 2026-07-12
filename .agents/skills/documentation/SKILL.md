---
name: documentation
description: Enforces high-quality, living documentation standards. Covers README structure, API clarity, and maintenance guidelines. Apply when writing or updating any documentation.
---

# Documentation Standards & Guidelines

## Guiding Principles

- **Documentation is part of the feature.** It should evolve with the code.
- **Never document features that do not exist.** Avoid speculative writing.
- **A new developer should be able to run the project without additional explanation.**

## README Structure

Follow this standard order to ensure consistency:

1. Project Overview
2. Features (Implemented only)
3. Architecture
4. Tech Stack
5. Project Structure
6. Installation
7. Configuration (Environment Variables)
8. Running the Application
9. API Documentation
10. Spatial Features (Sample GeoJSON)
11. Testing
12. Docker
13. Roadmap (Optional/Planned)
14. License

## Content Guidelines

- **Features:** List only implemented features. Do not list planned features unless explicitly marked in the Roadmap section.
- **Project Structure:** Document the purpose of each top-level folder (e.g., `app/routers/`). Avoid documenting individual files unless necessary.
- **Installation:** Commands must be copy-pasteable. Avoid placeholders.
- **Environment Variables:** Clearly document default, required, and optional values.

## API & Spatial Data

- **API Examples:** Include complete request and response examples. Prefer realistic data (actual GeoJSON structures) over placeholder values (e.g., "test").
- **Error Handling:** Document expected error responses (status codes and example payloads).
- **GeoJSON:** When documenting spatial data, always include: Geometry Type, CRS (e.g., EPSG:4326), Coordinate Order, and an example feature.
- **Versioning:** Document API version in one location only. Avoid duplication.

## Visuals & Diagrams

- **Mermaid:** Use diagrams (Sequence/Architecture) only when they improve understanding. Avoid diagrams for trivial workflows.
- **Complexity:** Keep diagrams simple and non-scrolling.

## Code-Level Documentation

- **Docstrings:** Write only when intent is not obvious. Explain the _Why_, not the _What_.
- **Comments:** Explain assumptions, trade-offs, or non-obvious decisions. Do not explain syntax.

## AI Behavior & Quality

- **Synchronization:** Keep documentation synchronized with the implementation.
- **No Speculation:** Do not generate documentation for endpoints that do not exist.
- **Readability:** Prefer short paragraphs and bulleted lists. Avoid walls of text.
- **Changelog:** Significant user-visible changes should be reflected in `CHANGELOG.md` if using semantic versioning.

## Self Review Checklist

- [ ] Can a new developer run the project without asking questions?
- [ ] Are all examples copy-pasteable and executable?
- [ ] Are all documented endpoints actually implemented?
- [ ] Is duplicated information avoided?
- [ ] Do GeoJSON examples include Type, CRS, and Coordinate Order?
- [ ] Is the architecture diagram accurate and concise?
