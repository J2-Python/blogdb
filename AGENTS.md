# AGENTS.md

## Repository Overview
- This repository is a small educational Django REST Framework blog project.
- The Django project root is `blogdj/`.
- The main app is `blogdj/applications/blog/`.
- Run Django commands from `blogdj/`, not from the repo root.
- Reason: `blogdj/settings/base.py` loads `secrets.json` with a relative path.

## Rule Sources
- `.cursor/rules/`: not present.
- `.cursorrules`: not present.
- `.github/copilot-instructions.md`: not present.
- There are no repo-specific AI rule files besides this `AGENTS.md`.

## Stack
- Python
- Django 5.2.12
- Django REST Framework 3.17.1
- PostgreSQL for local development
- SQLite in `blogdj.settings.test` for automated tests

## Important Paths
- Repo root: `/Users/juancollantes/Apps/Learning/blogdrf`
- Django root: `/Users/juancollantes/Apps/Learning/blogdrf/blogdj`
- App: `blogdj/applications/blog`
- Settings: `blogdj/blogdj/settings`
- Local settings: `blogdj/blogdj/settings/local.py`
- Test settings: `blogdj/blogdj/settings/test.py`
- Project urls: `blogdj/blogdj/urls.py`

## Environment Notes
- Activate the venv if needed: `source .venv/bin/activate`
- Install dependencies from repo root: `pip install -r requirements/local.txt`
- `manage.py` defaults to `blogdj.settings.local`.
- `blogdj/secrets.json` must exist for local commands.

## Run Commands
- `python manage.py runserver`
- `python manage.py runserver --settings=blogdj.settings.local`
- `python manage.py check`
- `python manage.py makemigrations`
- `python manage.py makemigrations blog`
- `python manage.py migrate`
- `python manage.py createsuperuser`

## Build, Lint, And Validation
- There is no frontend build step.
- There is no dedicated lint or formatter configured.
- Main validation command: `python manage.py check`
- Migration validation: `python manage.py makemigrations --check --dry-run`
- Main automated test command: `python manage.py test --settings=blogdj.settings.test`

## Test Commands
- Run all tests: `python manage.py test --settings=blogdj.settings.test`
- Run app tests: `python manage.py test --settings=blogdj.settings.test applications.blog`
- Run one test module: `python manage.py test --settings=blogdj.settings.test applications.blog.tests`
- Run one test class: `python manage.py test --settings=blogdj.settings.test applications.blog.tests.SeedBlogDataAPITests`
- Run one test method: `python manage.py test --settings=blogdj.settings.test applications.blog.tests.SeedBlogDataAPITests.test_seed_recreates_sample_data_with_default_count`

## Single-Test Guidance
- Start with the narrowest test that covers the change.
- For serializer or view work, prefer a single class or method first.
- If the focused test passes, run `applications.blog.tests` next.
- Run the full suite if settings or shared behavior changed.

## Project Structure
- `applications/blog/models.py`: domain models
- `applications/blog/serializers.py`: DRF serializers
- `applications/blog/views.py`: DRF views
- `applications/blog/urls.py`: app routes
- `applications/blog/tests.py`: app tests
- `applications/blog/services.py`: multi-step business logic

## Architecture Guidance
- Keep business logic out of views when several model writes are involved.
- Use serializers for validation and object creation.
- Use `services.py` for orchestration tasks such as seed/reset flows.
- Give new routes explicit names for `reverse()` lookups.
- Use transactions for destructive or multi-step write operations.

## Code Style
- Use 4-space indentation and standard Python formatting.
- Keep lines readable; no formatter is enforced today.
- Group imports into stdlib, Django/third-party, and local imports.
- Avoid unused imports.
- Prefer explicit imports over wildcard imports in app code.
- Keep constants in `UPPER_SNAKE_CASE`.
- Add docstrings for non-obvious modules, services, and endpoints.
- Add comments only when they clarify intent or constraints.

## Naming
- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- URL names: short, explicit, stable
- Serializers should reflect intent, e.g. `SeedBlogDataSerializer`.
- Views should reflect the action they perform.

## Types
- Type hints are encouraged for new helpers and services.
- Add return types when a helper returns structured data.
- Do not introduce heavy typing tooling unless requested.
- Match the repo's lightweight style.

## Django And DRF Conventions
- Prefer DRF generics such as `CreateAPIView` for standard CRUD.
- Prefer `APIView` for custom actions like seeding or resets.
- In custom views call `serializer.is_valid(raise_exception=True)`.
- Return explicit status codes with DRF `Response`.
- Use `reverse()` in tests instead of hardcoded URLs.
- Keep `queryset` defined on generic views when DRF expects it.

## Error Handling
- Do not use bare `except:` blocks.
- Raise `ValidationError`, `PermissionDenied`, or another framework-specific error.
- Wrap destructive multi-write operations in `transaction.atomic()`.
- Keep API messages clear and consistent with the language already used by the endpoint.
- Dangerous endpoints should fail closed. Example: seed/reset routes should be limited to `DEBUG` unless stronger protection is requested.

## Models And Migrations
- Do not casually rename persisted fields such as `Suscriptions` or `categorys`.
- Preserve existing APIs unless the task explicitly allows breaking changes.
- If models change, create migrations in the same change.
- Always run `python manage.py makemigrations --check --dry-run` before finishing model work.

## Testing Expectations
- Add tests for each new endpoint or service behavior.
- Cover the happy path and at least one guardrail or failure case.
- For debug-only endpoints, test both allowed and blocked behavior.
- Keep tests deterministic; avoid randomness unless tightly controlled.

## Repo Caveats
- `blogdj/settings/base.py` reads `secrets.json` from the current working directory.
- `requirements/test.txt` and `requirements/prod.txt` are empty.
- No linting, formatting, or static typing tool is configured.
- The project mixes Spanish domain text with Python identifiers.
- Educational clarity matters more than abstraction density.

## Working Style For Agents
- Expect a dirty worktree and do not revert unrelated user changes.
- Read local modifications before editing a touched file.
- Prefer the smallest correct change.
- Keep control flow obvious and educational.
- If you add a multi-table endpoint, put the write logic in a service function.
- If a non-model serializer is used with `CreateAPIView`, implement `create()`.
- After code changes, run the narrowest useful test and then a broader validation pass.

## Definition Of Done
- Code is understandable without extra explanation.
- Validation and error paths are explicit.
- Tests cover the new behavior.
- Commands in this file still match the repository layout.
- No unrelated files are modified.
