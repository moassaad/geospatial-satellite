---
name: ai-coding-rules
description: Strictly enforces AI behavior, operational scope, coding standards, and communication protocols. Apply this before generating any code or implementation to prevent hallucination, over-engineering, and scope creep.
---

# AI Coding & Operational Guidelines

## Guiding Principles

- **Do exactly what is asked. Nothing more, nothing less.**
- **Scope is sacred.** Do not modify files outside the requested scope.
- **Simplicity is the highest virtue.** Prefer simple solutions over complex ones.

## 1. Clarification & Uncertainty

- **Clarification Policy:** If required information is missing, ask a clarification question. Never guess requirements, APIs, or business rules.
- **Uncertainty:** When uncertain, prefer asking one clarification question instead of making assumptions.

## 2. Operational Scope & Editing

- **Minimal Editing:** Modify existing code whenever possible. Prefer patching over rewriting. Do not regenerate entire files for small changes.
- **Existing Code Wins:** Existing project conventions always take priority over generic best practices.
- **No Creativity:** Do not be creative. Do not redesign the project. Implement only the requested change.
- **Refactoring:** Refactor only when necessary to complete the requested task. Never refactor unrelated code.
- **Formatting/Names:** Preserve existing formatting, variable names, and class names unless explicitly requested. Do not reorder imports unless modifying them.

## 3. Implementation Rules

- **New Files/Dependencies:** Create new files only when required. Prefer existing project dependencies. Avoid introducing alternatives to libraries already used.
- **Configuration:** Do not modify configuration files (Docker, Alembic, pyproject, settings) unless required.
- **Tests:** Generate tests only when requested or when explicitly modifying tested code.
- **API Endpoints:** Do not generate CRUD endpoints automatically. Generate only requested endpoints.
- **Error Handling:** Do not silently ignore errors. Fail explicitly with meaningful exceptions.
- **Code Quality:** Generated code should be complete, correct, and executable. Avoid placeholder implementations (no TODO/pass).

## 4. Scope Expansion & Feedback

- **Scope Expansion:** When additional improvements are identified, mention them separately. Do not implement them.
- **Consistency:** When two implementations are equally valid, choose the one most consistent with the existing project.

## 5. Output Rules

- **Return only the requested output.**
- Do not include unrelated explanations.
- Do not repeat the prompt.
- Do not summarize generated code.
- Avoid unnecessary markdown.

## 6. Self-Audit Checklist (Pre-Generation)

- [ ] Did I preserve project conventions?
- [ ] Did I minimize the diff?
- [ ] Did I avoid unnecessary abstractions?
- [ ] Did I avoid speculative improvements/features?
- [ ] Did I clarify missing requirements instead of guessing?
- [ ] Is the code complete, correct, and executable?
