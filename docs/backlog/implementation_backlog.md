# Implementation backlog

This backlog is ordered for fastest delivery of the approved architecture.

## Epic A — Foundation
- Create Django 5.2 project on Python 3.14
- Add settings split: base / local / production
- Add PostgreSQL configuration
- Add health endpoints
- Configure structured logging
- Configure Django admin under `/gm/`
- Add base models: Event, Application, PaymentAttempt, Document, IntegrationEvent, AuditLog, Job
- Add migration pipeline
- Add CI checks (formatting, tests, migrations, import sanity)

## Epic B — Public site and form
- Port landing page from `reference/foreign_gates_v4.html`
- Move CSS into static assets
- Wire CTA to `/apply/`
- Add event config loader from YAML
- Add dynamic form schema loader from YAML
- Build server-side form renderer
- Persist normalized fields + `answers_json`
- Add confirmation page
- Add applicant confirmation email
- Add GM notification email
- Add honeypot anti-spam field
- Add optional rate limiting

## Epic C — GM workflow
- Register models in Django admin
- Add list filters and search
- Add read-only status summaries
- Add admin actions: approve, reject
- Add GM notes field
- Add public roster visibility fields
- Add audit logging for GM actions

## Epic D — Cardcom integration
- Create Cardcom service wrapper
- Implement `PaymentAttempt` creation
- Implement `/pay/<token>/` safe redirect route
- Implement payment-link email template
- Implement Cardcom webhook endpoint
- Persist raw Cardcom webhook payloads
- Implement DB-backed reconciliation job
- Implement `GetLpResult` verification
- Add idempotency guards
- Add admin action: resend payment link
- Add admin action: reconcile payment

## Epic E — Morning integration
- Create Morning service wrapper
- Implement `Document` persistence
- Implement post-payment document creation job
- Add retry behavior for failed document creation
- Add admin action: retry document creation
- Confirm live API request body against Morning docs
- Confirm send-by-email behavior against live API docs

## Epic F — Public roster
- Build `/players/` template
- Publish only approved public entries
- Hide paid status always
- Show character only when enabled
- Show faction only when enabled
- Default sort by display name

## Epic G — Operational hardening
- Add web and worker containers
- Add static asset collection step
- Add reverse proxy config
- Add backup policy if DB is project-owned
- Add sandbox credentials and environment separation
- Add alerting for failed jobs
- Add launch checklist
- Run full sandbox E2E

## Epic H — Launch
- Configure production DNS / TLS
- Configure Cardcom production callback URLs
- Configure Morning production API key
- Verify email delivery
- Run smoke test on live domain
- Enable registration
