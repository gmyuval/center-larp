# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Center LARP is a single-event LARP registration site for `center.larp.co.il`. Players apply, GMs approve/reject via Django admin, approved players pay through Cardcom hosted pages, and Morning (Green Invoice) generates accounting documents post-payment. A public roster shows published players.

**No source code exists yet** — the repo currently contains only the PRD/technical spec (`docs/Center_LARP_Handoff_Package.md`), example configs, ops templates, and an implementation backlog. The spec is the authoritative design document.

## Stack

- **Python 3.14**, **Django 5.2 LTS**, **PostgreSQL 18** (DigitalOcean managed cluster `db-postgresql-fra1-01`)
- Conda env: `conda env create -f environment.yml` (provides Python 3.14, pip-tools, pre-commit)
- Dependencies: `docs/ops/requirements.example.txt` (Django, gunicorn, psycopg3, httpx, django-environ, whitenoise, pydantic)
- Background jobs: DB-backed outbox + `manage.py run_jobs` worker (no Redis/Celery)
- Frontend: Django templates + vanilla JS, no SPA
- **Deployment**: DigitalOcean, `fra1` region. New `center_larp` database on existing managed PG cluster (SSL required, use private connection URI from within DO VPC).

## Planned Repo Structure

```text
manage.py
config/settings/{base,local,production}.py
config/{urls,wsgi,asgi}.py
apps/{public_site,applications,payments_cardcom,billing_morning,notifications,audit,jobs}/
templates/
static/
event_config/{current_event.yaml,application_form.yaml}
```

## Key Commands (once scaffolded)

```bash
python manage.py runserver              # local dev server
python manage.py migrate                # apply migrations
python manage.py run_jobs               # start background worker
python manage.py collectstatic --noinput
python manage.py test                   # run tests
docker compose -f ops/docker-compose.example.yml up  # full stack
```

## Architecture Essentials

- **Cardcom Low Profile** for payments — never store card data; always verify server-side via `GetLpResult`; browser return pages are informational only
- **Morning API** for accounting docs (type 320 default) — created only after verified payment; one document per payment attempt max
- **Django admin at `/gm/`** is the GM backoffice — no custom dashboard in v1
- **YAML-driven config**: event metadata in `current_event.yaml`, form schema in `application_form.yaml` — avoids migration churn
- **Approval-first flow**: payment links sent only after GM approval, not at checkout

## Critical Business Rules

- Payment status transitions only on server-side Cardcom verification, never from browser redirect
- Duplicate webhook deliveries must be idempotent (dedupe via `IntegrationEvent.dedupe_key`)
- Only one active `PaymentAttempt` per application at a time
- Public roster never exposes: paid status, email, phone, notes, invoice info
- Character/faction visibility require explicit GM toggles (default off)
- Player-facing payment URLs use `/pay/<token>/` (site-owned), never raw Cardcom URLs

## External Services

- **Cardcom**: `POST /api/v11/LowProfile/Create`, `GET /api/v11/LowProfile/GetLpResult`
- **Morning (Green Invoice)**: document creation API, sandbox available for testing
- Webhook endpoints: `/webhooks/cardcom/low-profile/` and `/webhooks/morning/document-created/` (both CSRF-exempt)

## Development Workflow

- **Branching**: Always work on `feature/` or `bug/` branches off `main`. Never commit directly to `main`.
- **Review before commit**: When development is complete, present a summary of files added/modified and what was done. Wait for explicit user approval before committing.
- **After approval**: Commit, push, and create a PR on GitHub.
- **PR size**: Target 500-800 lines per PR. Break larger work into multiple PRs if needed.
- **Tooling priority**: Use the DigitalOcean and GitHub MCP tools as the first option. Fall back to `doctl` and `gh` CLI only if MCPs don't work. Use Context7 MCP for library/API documentation reference.
- **Conda environment**: Use the `center-larp` conda env. Activate with `conda activate center-larp`. All Python/pip commands should run inside this env.
- **OOP**: Follow OOP best practices throughout. Use classes and methods; avoid top-level functions unless strictly necessary (e.g., Django's `urlpatterns`, simple config).

## Dependency Management

- **`pyproject.toml`** is the single source of truth for all project metadata, dependencies, and tool configuration.
- **pip-tools** generates frozen/locked requirements from `pyproject.toml`:
  - `pip-compile pyproject.toml -o requirements.txt` for the base locked set
  - `pip-compile pyproject.toml --extra dev -o requirements-dev.txt` if dev extras are defined
- **`environment.yml`** should be updated to reflect changes — add conda-native packages there when appropriate, and reference the pip-tools output for pip dependencies.
- **Workflow when adding/changing a dependency**: edit `pyproject.toml` → run `pip-compile` → update `environment.yml` if needed → commit all three files together.

## Language and Locale

- Public pages are **Hebrew RTL**
- Timezone: `Asia/Jerusalem`
- Currency: ILS
