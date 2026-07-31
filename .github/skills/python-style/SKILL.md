---
name: python-style
description: Enforces clean, Pythonic, and strict coding standards for Python 3.12+. Apply this when writing, refactoring, or reviewing Python code to ensure readability, robust type hinting, and maintainability.
---

# Python Style & Clean Code Guidelines

## Target Python Version

- **Target Python:** 3.12+
- Use only features available in Python 3.12 or earlier.
- Prefer modern syntax introduced in Python 3.10+ such as:
  - `match`/`case` when appropriate.
  - `X | None` instead of `Optional[X]`.
  - `list[str]` instead of `List[str]`.

## Readability First

When multiple Python solutions exist, choose the one that is easiest to understand. Pythonic code should never sacrifice clarity for cleverness.

## The Pythonic Way

- **Truthiness:** Use Python truthiness naturally. Prefer `if value:` instead of `if value is not None and len(value) > 0:` unless explicit distinction is required.
- **Boolean Expressions:** Prefer direct boolean expressions. Good: `if items:`. Bad: `if len(items) > 0:`.
- **Comprehensions:** Use list/dict/set comprehensions when they improve readability. Avoid nested comprehensions that reduce clarity.
- **Context Managers:** Always use `with` statements for resource management (files, network connections, database sessions).
- **String Formatting:** Exclusively use f-strings (`f"{variable}"`).

## Type Hinting (Strict)

- **Mandatory:** All function arguments and return values MUST have explicit type hints.
- **Avoid `Any`:** Use `Any` only as an absolute last resort. If `Any` is required, document why.

## Data Structures & State

- **Collections:** Prefer built-in collections. Avoid unnecessary conversions. Choose the simplest data structure that fits the problem.
- **Immutability:** Prefer immutable objects when practical. Avoid mutating function arguments.
- **Dataclasses vs Pydantic:**
  - Use `dataclasses` only for lightweight data containers.
  - Use Pydantic models for API requests, API responses, and Configuration.
  - Do NOT replace Pydantic models with dataclasses inside API boundaries.
  - Avoid passing plain dictionaries across application boundaries.

## Standard Library Preferences

- **Paths:** Prefer `pathlib` for filesystem operations. Use `os` only when required by external libraries or platform-specific behavior.
- **Enums:** Use `Enum` when representing a finite domain of related values. Do not create an `Enum` for simple constants (e.g., `CONTENT_TYPE = "application/json"`).

## Functions & Control Flow

- **Design:** Keep functions focused. Split functions only when readability improves. Avoid excessive fragmentation.
- **Execution:** Validate inputs and fail fast. Prefer early returns to avoid nested conditions.

## Error Handling & Exceptions

- **Specific Catching:** Catch explicit, specific exceptions. Never use a bare `except:`.
- **Raising Errors:** Raise meaningful exceptions. Never raise generic `Exception`. Prefer custom domain exceptions when appropriate.
- **Never Suppress:** Never silently suppress errors with `pass` unless explicitly justified.

## Logging

- Use the `logging` module.
- Never `print()`.
- Log meaningful context.
- Avoid logging sensitive information.
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR).

## Docstrings & Comments

- **Docstrings:** Use docstrings ONLY when necessary. Do not write redundant docstrings that just repeat the function name.
- **Self-Documenting Code:** Code should explain _what_ and _how_. Comments should only explain _why_.

## Naming, Constants & Imports

- **Naming:** Variables and functions must reveal intent.
- **Constants:** Avoid "magic numbers" and "magic strings". Centralize constants in `UPPER_SNAKE_CASE`.
- **Imports:** Group imports logically, separated by one blank line:
  1. Standard library
  2. Third-party
  3. Local project imports

## Performance

- Do not optimize prematurely.
- Favor readability.
- Optimize only when profiling indicates a bottleneck.

## Forbidden Practices

- Never use wildcard imports (`from module import *`).
- Never use mutable default arguments (`def func(items=[]):`). Use `items: list[str] | None = None`.
- No obvious comments, commented-out code, `TODO`s, or placeholders in generated code.
- Never leave unused imports or unused variables.

## AI Scope & Implementation Rules

- Modify ONLY requested code.
- Preserve existing style.
- Avoid introducing abstractions.
- Generate the minimum necessary changes.
- Do not rewrite unrelated code.

## AI Implementation Checklist

- [ ] Code is formatted strictly to PEP8 standards.
- [ ] Type hints are 100% complete with modern Python 3.12+ syntax.
- [ ] Truthiness and boolean expressions are idiomatic.
- [ ] `pathlib` and `Enum` are used appropriately (not forced).
- [ ] Import grouping is correct.
- [ ] Unused imports, dead code, and placeholders are removed.
- [ ] Output contains minimal necessary changes.
