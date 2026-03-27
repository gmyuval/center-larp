# Implementation Plan

This plan breaks the project into PRs targeting 500-800 lines each, following the architecture defined in `Center_LARP_Handoff_Package.md` and the epic ordering from `backlog/implementation_backlog.md`.

---

## Phase 0 — Foundation

### PR 1: Project Scaffold & Configuration (~600-700 lines) ✅

**Branch:** `feature/project-scaffold`

Deliverables:
- `pyproject.toml` — project metadata, dependencies, tool config (ruff, pytest, etc.)
- `pip-compile` output -> `requirements.txt`
- Updated `environment.yml` with pip reference
- `manage.py`
- `config/` — settings split (`base.py`, `local.py`, `production.py`), `urls.py`, `wsgi.py`, `asgi.py`
- Empty app shells (`apps/` with `__init__.py` + `apps.py` for each of: `public_site`, `applications`, `payments_cardcom`, `billing_morning`, `notifications`, `audit`, `jobs`)
- Health endpoints (`/health/live/`, `/health/ready/`)
- `ops/Dockerfile`, `ops/docker-compose.yml` (promote from examples to real files)
- `.pre-commit-config.yaml`

Acceptance:
- `python manage.py check` passes
- Health endpoints return 200 / 503 as expected
- Docker build succeeds
- `pip-compile` output is committed and reproducible

---

### PR 2: Core Data Models & Migrations (~600-750 lines) ✅

**Branch:** `feature/core-models`

Deliverables:
- `Event` model — slug, title, price, currency, registration flags, Morning doc type
- `Application` model — public_id (UUID), normalized contact fields, `answers_json` (JSONB), `gm_status`, `payment_status`, `invoice_status`, visibility toggles, timestamps
- `PaymentAttempt` model — public_id (UUID), vendor fields, status, raw JSON responses; constraint: one active attempt per application
- `Document` model — vendor doc id, type, number, status; unique on `payment_attempt_id`
- `IntegrationEvent` model — source, event_type, dedupe_key, processing status; unique on `source + dedupe_key`
- `AuditLog` model — actor, action, target, details JSON
- `Job` model — queue, type, payload, dedupe_key, status, retry tracking
- Initial migrations for all models
- Basic admin site registration for all models (minimal, expanded in PR 5)

Acceptance:
- `python manage.py migrate` runs cleanly
- All models visible in `/gm/` admin
- Constraints enforced at DB level

---

## Phase 1 — Public Site

### PR 3: Config Loaders & Landing Page (~600-800 lines) ✅

**Branch:** `feature/landing-page`

Deliverables:
- Pydantic-based YAML config loader for `current_event.yaml`
- Pydantic-based YAML schema loader for `application_form.yaml`
- Move example YAMLs into `event_config/` as working configs
- Landing page Django template (ported from `reference/foreign_gates_v4.html`)
- Extracted static CSS file (from inline styles in reference HTML)
- Landing page view class, parameterized from YAML config
- URL wiring for `/`

Acceptance:
- Landing page renders on desktop and mobile (RTL Hebrew intact)
- Event metadata (title, dates, price, factions) comes from YAML, not hardcoded
- CTA links to `/apply/`

---

### PR 4: Application Form & Submission Flow (~600-800 lines) ✅

**Branch:** `feature/application-form`

Deliverables:
- Dynamic form class built from YAML schema at runtime
- Server-side validation (required fields, email format, phone)
- Honeypot anti-spam field
- `/apply/` view class (GET renders form, POST validates and saves)
- `/apply/thanks/` confirmation page template
- Email: applicant confirmation
- Email: GM new-application notification
- Email templates (plain Hebrew)

Acceptance:
- Valid submission creates `Application` record with normalized fields + `answers_json`
- Invalid submission shows validation errors, no record created
- Honeypot triggers rejection
- Confirmation and GM notification emails sent
- Tests: A4, A5, A6 from acceptance matrix

---

## Phase 2 — GM Workflow

### PR 5: Admin Customization & Audit Logging (~500-700 lines) ✅

**Branch:** `feature/gm-workflow`

Deliverables:
- `ApplicationAdmin` — list display with status columns, filters by `gm_status` / `payment_status` / `invoice_status`, search by name / email / phone
- Custom admin actions: approve, reject (with state transition guards)
- GM notes field in admin detail view
- Public roster visibility toggles (publish/unpublish, character, faction) in admin
- Read-only inlines for `PaymentAttempt`, `Document` on Application detail
- `AuditLog` helper class for recording GM and system actions
- Audit entries written on approve / reject / visibility changes

Acceptance:
- GM can approve and reject from list view
- Filters and search work
- Audit log records all GM actions
- Tests: B1-B5 from acceptance matrix

---

## Phase 3 — Deployment (Early)

### PR 6: Infrastructure & Initial Deployment (~400-600 lines)

**Branch:** `feature/infra-deployment`

Deliverables:
- Droplet provisioning (`s-1vcpu-2gb`, fra1, default-fra1 VPC) via DO MCP or doctl
- `center_larp` database + dedicated user on existing managed PG cluster
- DNS: DigitalOcean A record for `center.larp.co.il` pointing to droplet public IP
- SSL via Let's Encrypt (certbot on nginx)
- Docker image build + push to DigitalOcean Container Registry (`registry.digitalocean.com/praxiscode/center-larp`)
- `ops/docker-compose.prod.yml` — production compose file using `image:` from DOCR
- Finalized `ops/nginx.center.larp.co.il.conf` with SSL + reverse proxy
- `ops/.env.example` updated with all current production variables
- GitHub secrets configured for deployment credentials
- Manual deploy (SSH + docker compose pull + up)

Acceptance:
- `https://center.larp.co.il/health/live/` returns 200
- `https://center.larp.co.il/health/ready/` returns 200 (DB connected)
- GM admin accessible at `/gm/`
- Public landing page renders correctly
- Webhook URL reachable from external services

---

## Phase 4 — Payments

### PR 7: Cardcom Integration — Payment Creation & Webhook (~600-800 lines)

**Branch:** `feature/cardcom-integration`

Deliverables:
- `CardcomService` class (`create_payment_page`, `verify_payment`)
- `PaymentAttempt` creation flow (sets `public_id` as Cardcom `ReturnValue`)
- `/pay/<token>/` safe redirect view (resolves active attempt, redirects to Cardcom URL)
- Payment link email template
- Cardcom webhook endpoint (`/webhooks/cardcom/low-profile/`, CSRF-exempt)
- `IntegrationEvent` persistence on webhook receipt (return HTTP 200 quickly)
- Admin action: generate payment link
- Admin action: resend payment link (invalidates previous active attempt)

Acceptance:
- Payment link creation calls Cardcom API, stores response, emails player
- `/pay/<token>/` redirects to Cardcom hosted page
- Webhook persists raw payload and returns 200
- Invalidated links are blocked on open
- Tests: C1, C2, C4, C8 from acceptance matrix

---

### PR 8: Job Runner & Payment Verification (~500-700 lines)

**Branch:** `feature/payment-verification`

Deliverables:
- DB-backed job runner management command (`run_jobs`) with polling loop and locking
- Job dispatch and dead-letter logic
- Payment reconciliation job (calls `GetLpResult`, checks `ResponseCode == 0`)
- Idempotency guards (already-paid check, dedupe key on `IntegrationEvent`)
- Mark `PaymentAttempt` + `Application` as paid on verified success
- Enqueue Morning document creation job on verified payment
- `/payment/return/success/` and `/payment/return/failure/` informational pages
- Admin action: manually reconcile payment
- Audit log entries for payment verification events

Acceptance:
- Worker picks up and processes queued jobs
- Verified payment transitions attempt and application to paid
- Duplicate webhook does not create duplicate state change
- Browser return pages are informational only (no state change)
- Tests: C3, C5, C6, C7 from acceptance matrix

---

## Phase 5 — Billing

### PR 9: Morning Integration (~500-650 lines)

**Branch:** `feature/morning-integration`

Deliverables:
- `MorningBillingService` class (`create_document`, `get_document`)
- Document creation job (triggered after verified payment)
- Field mapping: application -> Morning recipient, event -> line item, Cardcom tx -> payment reference
- `Document` record persistence with status tracking
- Retry logic for failed document creation (exponential backoff in job runner)
- Admin action: retry document creation
- Email-send behavior (via Morning send-on-create or app-triggered second call)
- Audit log entries for document creation events

Acceptance:
- Verified payment triggers exactly one document creation
- Failed creation retries without duplicates
- Admin retry produces document if API recovers
- Tests: D1-D4 from acceptance matrix

---

## Phase 6 — Public Roster & Hardening

### PR 10: Public Roster, Mobile Responsiveness & Logging (~500-700 lines)

**Branch:** `feature/public-roster`

Deliverables:
- `/players/` view class — queries only published applications
- Roster template (display name always; character and faction only if toggled on)
- Visibility rules enforced at query level (never expose paid status, email, phone, notes)
- Alphabetical sort by display name
- Mobile responsiveness audit and fixes across all public pages (landing, apply, thanks, roster)
- Structured JSON logging configuration in settings
- Final `ops/.env.example` update

Acceptance:
- Published player shows display name; character/faction only when enabled
- Unpublished player absent from roster
- Paid status never visible
- All public pages render correctly on mobile phones and tablets
- Tests: E1-E5, F4 from acceptance matrix

---

## Phase 7 — Authentication

### PR 11: Google OAuth for Admin Login (~300-400 lines)

**Branch:** `feature/google-oauth`

Deliverables:
- `django-allauth` added to dependencies with Google OAuth provider
- Settings configuration for allauth (Google client ID + secret from env vars)
- URL wiring for `/accounts/` allauth routes
- Admin login integration (GM login via Google account)
- Migration for allauth tables

Acceptance:
- GMs can log into `/gm/` using their Google account
- Traditional username/password login still works as fallback
- OAuth credentials are externalized as env vars

---

## Dependency Graph

```text
PR 1 (scaffold)
  └─> PR 2 (models)
        └─> PR 3 (config + landing)
              └─> PR 4 (form + submission)
                    └─> PR 5 (GM workflow)
                          └─> PR 6 (infra + deploy)
                                ├─> PR 7 (Cardcom creation + webhook)
                                │     └─> PR 8 (job runner + verification)
                                │           └─> PR 9 (Morning) [parallel with PR 10]
                                ├─> PR 10 (roster + mobile + hardening) [parallel with PR 9]
                                └─> PR 11 (Google OAuth)
```

PRs 9 and 10 are independent of each other and can be developed in parallel.
PR 11 (Google OAuth) can be done at any point after PR 6.

---

## Open Items (must be resolved before relevant PR)

| Item | Blocking PR | Owner | Status |
|------|-------------|-------|--------|
| Final application form questions | PR 4 | GMs | ✅ Resolved (matched to Google Form) |
| Final Morning document type (320 vs 305 vs 400) | PR 9 | Accountant | Open |
| Live Morning API create-document request shape | PR 9 | Dev (read live docs) | Open |
| GM notification target (mailbox / list / chat) | PR 4 | GMs | ✅ Resolved |
| DigitalOcean API token + SSH key for deployment | PR 6 | DevOps | ✅ Resolved |
| Cardcom terminal number + API credentials | PR 7 | DevOps | ✅ Resolved |
| Resend API key for email | PR 7 | DevOps | ✅ Resolved |
| Google Cloud OAuth client ID + secret | PR 11 | DevOps | Open — provide before PR 11 |
