# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**HelpDesk Hub API** is a backend API for internal helpdesk ticket management built with FastAPI, Pydantic, and Python 3.10+. The project evolves incrementally following Spec-Driven Development (SDD), progressing from simple in-memory features to a production-grade system with persistence, authentication, observability, and CI/CD.

**Key traits:**
- Clean Architecture with clear separation between API, Application, Domain, and Infrastructure layers
- SOLID principles and guard clauses for code clarity
- Specification-first approach documented in `docs/spec-driven-development.md`
- TDD-driven, all features covered by automated tests
- Managed with `uv` for dependencies and Python tooling

## Project Structure

After the Clean Architecture refactor, the structure is:

```
src/
├── main.py                 # FastAPI app factory
├── api/                    # HTTP layer (routes, schemas)
│   ├── routes.py          # API endpoints
│   └── schemas/           # Pydantic request/response models
│       ├── system.py      # Health, root endpoints
│       └── ticket.py      # Ticket DTOs
├── application/           # Use cases & business logic (planned)
├── domain/                # Domain entities & rules
│   └── enums.py          # TicketStatus, TicketPriority, TicketCategory
└── infrastructure/        # DB, external services (planned)
```

**Import convention:** Paths are relative to `src/` (configured in `pyproject.toml` under `tool.pytest.ini_options.pythonpath`). Import as `from api.routes import ...`, not `from helpdesk_hub_api.api.routes import ...`.

## Common Commands

**Setup & Dependencies**
```bash
uv sync                                    # Install all dependencies
```

**Running the App**
```bash
uv run uvicorn main:app --reload          # Start dev server (auto-reload on file changes)
```
App runs at `http://127.0.0.1:8000`. Interactive docs at `/docs` (Swagger UI).

**Testing**
```bash
uv run pytest                              # Run all tests
uv run pytest tests/test_app.py           # Run a single test file
uv run pytest tests/test_app.py::test_root_endpoint_returns_project_metadata  # Run a single test
uv run pytest -v                           # Verbose output
```

All tests must pass before creating a commit. Tests are located in `tests/` and use FastAPI's `TestClient`.

## Architecture Directives

These principles guide all implementation:

1. **Clean Architecture**: Respect layer separation. API layer handles HTTP concerns only (routing, serialization). Domain layer contains business rules and enums. Application layer (when needed) will hold use cases. Infrastructure layer (when needed) will handle persistence and external integrations.

2. **SOLID Principles**: Favor composition over inheritance, depend on abstractions, keep functions focused on one responsibility.

3. **DRY & Guard Clauses**: Avoid duplication. Use guard clauses (`if x: return`) to keep logic flat and readable instead of nested conditionals.

4. **Transversal Concerns**: Use middlewares for cross-cutting issues (logging, auth, error handling) rather than scattering them across routes.

5. **Design Patterns**: Apply patterns (e.g., Repository, Service, Factory) only when solving real problems, not for theoretical completeness.

## Development Workflow

This project uses **Spec-Driven Development (SDD)**:

1. **Before coding**: Write or refine a spec in `docs/features/f0XX-<feature-name>.md` (use `docs/features/_template.md` as a template).
2. **Spec content**: Problem statement, business context, acceptance criteria, technical impacts, and implementation plan.
3. **Feature tracking**: Index all specs in `docs/spec-driven-development.md`. Map specs to GitHub issues.
4. **Implementation**: Follow the spec. Update it with decisions and final status when done.
5. **PR/Commit**: Reference the spec (e.g., `closes #123, implements F009`) and link to the feature document.

See `docs/spec-driven-development.md` for detailed guidance, the project roadmap (11 phases), and feature index.

## Git Workflow & Branching

All features follow a standardized branching and commit strategy:

**Branch naming:** `feature/f<numero>-<slug>`

- Example: `feature/f008-create-schema-ticket`
- Always branch from `develop`, never from `main`

**Commit messages:** `[FNUMERO] Brief description`

- Example: `[F008] Add TicketCreate schema with validation`
- Keep commits atomic (one logical change per commit)
- All tests must pass before pushing

**Pull Requests:**

- Title format: `[FNUMERO] Feature description`
- Always target `develop` branch, not `main`
- Include: what changed, why, and acceptance criteria met
- Reference the GitHub issue: `closes #9`
- Require code review before merge

**Merge strategy:** Squash and Merge

- Keeps main/develop history clean
- Squash message: `[FNUMERO] Complete feature description`

**After merge:**

- Update the feature spec with PR link: `- PR: #<numero>`
- Update status to `Done`
- Record final decisions in spec

## Key Files & References

| File | Purpose |
| --- | --- |
| `README.md` | Project overview, quick start, endpoints |
| `docs/spec-driven-development.md` | SDD guide, roadmap, feature index, naming conventions |
| `docs/features/` | Feature specifications and decisions |
| `pyproject.toml` | Dependencies, build config, pytest configuration |
| `src/main.py` | FastAPI app factory |
| `tests/` | Test suite (TDD-driven) |

## Testing Strategy

- All new features must have passing tests before merge.
- Tests follow TDD: write spec/test first, then implementation.
- Use `TestClient` from FastAPI for HTTP testing.
- Tests run via `pytest` with paths configured to `src/` for clean imports.
- Test files are in `tests/` and should mirror the structure being tested (e.g., `test_app.py` for `src/main.py`).

## Notes for Future Instances

- **Phase 1 (current)**: Foundation. Endpoints, schemas, domain enums, Clean Architecture structure. No persistence or auth yet.
- **Upcoming phases**: Persistence (PostgreSQL + SQLAlchemy), user management, JWT auth, business logic, testing suite, Docker, CI/CD, observability.
- **Avoid over-engineering**: Features start simple (in-memory) and evolve. Don't add patterns or layers before they're needed.
- **Check the spec first**: If a task feels ambiguous, check `docs/features/` or `spec-driven-development.md` for context and decisions.

## Troubleshooting

- **Import errors**: Ensure you're in the root of the project when running tests. Paths are relative to `src/`. Check `pythonpath` in `pyproject.toml`.
- **Tests fail after refactor**: Update imports to use new path structure (e.g., `from api.schemas.ticket import ...` instead of `from helpdesk_hub_api.schemas.ticket import ...`).
- **Uvicorn won't reload**: Make sure you're running with `--reload` flag. Check for syntax errors in modified files.
