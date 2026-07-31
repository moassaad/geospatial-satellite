---
name: git-workflow
description: Enforces version control best practices, Conventional Commits, atomic changes, and branching strategies. Apply when generating commit messages, Git commands, or code review strategies.
---

# Git & Version Control Guidelines

## Guiding Principles

- **Git history should tell the story of the project.** It should read like a clear, chronological log of what changed and why.
- **Every commit should have a clear purpose.** A single commit should represent exactly one logical change.
- **Milestone Integrity:** Each project milestone should end with a working commit. Never leave the repository in a broken state.

## Conventional Commits

- **Format:** Adhere strictly to the Conventional Commits specification (`type(scope): description`).
- **Types:** `feat`, `fix`, `refactor`, `chore`, `docs`, `test`.
- **Imperative Mood:** Always write the description in the imperative, present tense (e.g., "Add endpoint", not "Added").
- **Dependency Updates:** Dependency upgrades should use `chore(deps):`.
- **Breaking Changes:** When introducing breaking changes, use the Conventional Commits `BREAKING CHANGE` footer.

## Commit Scope & Body

- **Commit Scope:** Use a meaningful scope when it improves clarity. Avoid meaningless scopes. Examples:
  - `feat(api): add region upload endpoint`
  - `fix(repository): handle missing geometry`
  - `docs(readme): update setup instructions`
- **Commit Body:** Provide a detailed explanation in the commit body if the "why" is not obvious. Example:

  ```text
  feat(api): add GeoJSON upload endpoint

  Support importing regions from GeoJSON files.
  Validation occurs before persistence to prevent invalid geometries from reaching PostGIS.
  ```

## Atomic Changes & Commit Size

- **Single Responsibility:** Do not mix different concerns. Avoid extremely large commits. Prefer several logical commits over one massive commit.
- **Formatting Rule:** Formatting-only changes should be committed separately.
- **Rename Rule:** File renames should be committed separately when they are unrelated to logic changes.
- **Documentation:** Documentation updates should accompany user-visible behavior changes when necessary.

## Branching Strategy

- **Protected Branches:** Never commit directly to the main branch.
- **Naming Conventions:** Preferred branch categories: `feature/`, `fix/`, `refactor/`, `docs/`, `test/`, `chore/`.

## Artifacts & Git Ignore

- **Generated Files:** Do not commit generated artifacts unless explicitly required (e.g., `__pycache__`, compiled files, temporary outputs).
- **.gitignore:** Keep `.gitignore` clean. Ignore development artifacts, secrets, virtual environments, and local IDE files.

## Pull Requests, Rebasing & Merging

- **Rebase Rule:** Prefer rebasing local feature branches before opening pull requests to minimize unnecessary merge commits.
- **Merging & History:** Choose the merge strategy that preserves a clean and understandable history. Avoid unnecessary merge commits.

## Tags & Releases

- **Semantic Versioning:** Release tags should point to immutable production-ready commits.

## AI Decision Rules

If several commit messages are valid, prefer the one that:

1. Explains intent.
2. Is concise.
3. Follows Conventional Commits.
4. Avoids unnecessary wording.

## Self Review Checklist

- [ ] Commit message follows the `type(scope): description` format.
- [ ] Commit body provides context when needed.
- [ ] The suggested commit represents a single, atomic change.
- [ ] Formatting changes and file renames are not mixed with logic.
- [ ] No generated files or secrets are included.
- [ ] The repository is left in a working state.
