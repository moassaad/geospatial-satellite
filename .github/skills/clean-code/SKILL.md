---
name: clean-code
description: Enforces advanced clean code philosophy, abstraction levels, and maintainability. Apply this to identify code smells, simplify logic, and ensure high readability beyond basic syntax.
---

# Advanced Clean Code Guidelines

## Core Principles

- **SOLID, DRY, KISS, YAGNI:** Apply strictly, but pragmatically.
- **Readable code is more valuable than compact code.**
- **Code explains WHAT; Comments explain WHY.**

## Levels of Abstraction

- **One Level:** A function should operate at a single level of abstraction. Avoid mixing high-level orchestration with low-level implementation details in the same function.
- **Helper Functions:** Prefer extracting intent-revealing helper functions instead of nesting logic.

## Function Design

- **Arguments:** Prefer small parameter lists. More than four parameters usually indicate that a value object or schema should exist.
- **Boolean Parameters:** Avoid boolean parameters. Instead of `create_user(is_admin=True)`, prefer `create_admin()` or passing a configuration object.
- **Return Values:** Prefer returning explicit values. Avoid returning multiple unrelated values or `None` if an exception better communicates failure.
- **Side Effects:** Functions should minimize side effects. Ideally, a function should either perform an action (Command) or compute a value (Query).

## Conditionals & Control Flow

- **Simplicity:** Reduce nested `if` statements. Prefer early returns.
- **Polymorphism:** Prefer polymorphism over long `switch` or `if/else` chains when logic complexity grows.
- **Exceptions:** Use exceptions for exceptional situations. Avoid using exceptions for normal control flow.

## Duplication & Reuse

- **Duplicated Knowledge:** Avoid duplicated _knowledge_, not merely duplicated lines. Two identical lines are acceptable if extracting them into a common utility harms readability.
- **Clever vs Explicit:** Prefer explicit code over clever code.

## Code Smells (The Watch List)

During review, identify and address these smells:

- Long functions
- Long parameter lists
- Deep nesting (Arrow code)
- Large classes (God objects)
- Duplicated knowledge
- Feature envy (Method calls another class's data more than its own)
- Primitive obsession (Overuse of basic types instead of custom objects)
- Temporary variables (used for intermediate state instead of direct return)
- Excessive comments (indicating code is hard to read)
- Magic values (numbers/strings without context)

## AI Behavior & Scope

- **Strict Scope:** Never improve code outside the requested scope. Do not "clean up" unrelated files, rename variables, or reorder code without a specific reason related to the task.
- **Refactoring:** Refactor only when it improves readability and maintainability.
- **YAGNI Implementation:** Do not implement pagination, authentication, caching, configuration, or extension points until explicitly required by the task.

## Self Review Checklist

- [ ] Does every function work at one single abstraction level?
- [ ] Is there any duplicated _knowledge_?
- [ ] Are there unnecessary abstractions or over-engineering?
- [ ] Is the parameter list short?
- [ ] Are there hidden side effects?
- [ ] Can nested conditions be simplified via early returns?
- [ ] Did I touch any code outside the requested scope?
