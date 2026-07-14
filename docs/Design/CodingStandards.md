# Coding Standards

## Purpose
These standards define how the project should be implemented and maintained so that it remains understandable, testable, and suitable for collaborative or agent-assisted development.

## Core principles
- Keep the domain model explicit and readable.
- Prefer clear, small functions over large, complex ones.
- Validate all state-changing actions on the server.
- Write tests for game rules, scoring logic, and persistence behavior.
- Keep documentation aligned with implementation.

## Language and tooling
- Use Python for backend implementation.
- Use TypeScript for frontend implementation when applicable.
- Follow conventional formatting and linting rules.
- Keep dependencies limited to what the product needs.
- Track Python dependencies in requirements.txt and scan them regularly.

## Naming conventions
- Use descriptive names for domain objects and services.
- Use lowercase snake_case for Python files, variables, and functions.
- Use PascalCase for classes and TypeScript types.
- Use clear names for game concepts such as game, turn, score_card, and score_entry.

## Architecture conventions
- Keep business rules in service-layer code rather than UI-layer code.
- Keep persistence concerns separate from domain logic where practical.
- Make game state transitions explicit and observable.
- Avoid duplicating scoring logic across frontend and backend.

## File organization
A proposed structure is:
- app/ for application code
- domain/ for core game concepts
- services/ for orchestration and business rules
- api/ for request handlers
- models/ for persistence models
- tests/ for automated tests

## Testing expectations
Every significant change should include tests for:
- scoring calculations
- turn progression
- invalid move handling
- persistence and retrieval of game state

## Documentation expectations
- Update the relevant documentation whenever behavior changes.
- Keep the PRD, architecture, database, and roadmap aligned with implementation.
- Record major design decisions in a structured format.

## Containerization expectations
- Keep the application container-friendly by using environment-based configuration and a single entrypoint.
- Prefer Dockerfiles that install dependencies from requirements and expose the app on a standard port.
- Support local development with docker compose and keep the setup suitable for future remote container hosting.

## Change management expectations
- Keep commits focused and descriptive.
- Do not combine unrelated functional changes in one change set.
- Prefer small iterations that can be reviewed easily.

## Quality bar for completion
A feature is not complete until:
- it works in the intended scenario
- it is covered by relevant tests
- its documentation is updated
- it follows the agreed architectural boundaries
