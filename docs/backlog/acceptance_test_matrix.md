# Acceptance test matrix

## A. Public flow

| ID | Scenario | Expected result |
|---|---|---|
| A1 | Open `/` on desktop | Landing page renders correctly, RTL intact, CTA visible |
| A2 | Open `/` on mobile | Layout remains readable, no broken sections |
| A3 | Click CTA | User reaches `/apply/` |
| A4 | Submit valid application | Record created, user sees thanks page, emails sent |
| A5 | Submit invalid application | Validation errors shown, no record created |
| A6 | Trigger honeypot | Submission blocked or silently discarded per policy |

## B. GM workflow

| ID | Scenario | Expected result |
|---|---|---|
| B1 | GM opens `/gm/` | Admin loads and only staff access is allowed |
| B2 | GM approves application | `gm_status=approved`, audit entry written |
| B3 | GM rejects application | `gm_status=rejected`, audit entry written |
| B4 | GM toggles public visibility | Public roster reflects new state |
| B5 | GM toggles character/faction | Public roster shows only enabled fields |

## C. Cardcom integration

| ID | Scenario | Expected result |
|---|---|---|
| C1 | GM generates payment link | `PaymentAttempt` created, link email sent |
| C2 | Player opens `/pay/<token>/` | Redirects to current Cardcom page |
| C3 | Successful payment browser return only | App shows informative page but does not mark paid yet |
| C4 | Cardcom webhook received | Raw event stored, HTTP 200 returned quickly |
| C5 | Worker verifies with `GetLpResult` success | Attempt becomes paid, application paid timestamp set |
| C6 | Duplicate webhook delivery | No duplicate payment state change, no duplicate document |
| C7 | Failed / cancelled payment | Attempt becomes failed or remains unpaid per reconciliation result |
| C8 | Old invalidated payment link opened | App blocks or redirects to a fresh path per policy |

## D. Morning integration

| ID | Scenario | Expected result |
|---|---|---|
| D1 | Verified payment triggers document creation | One `Document` record created |
| D2 | Morning API temporary failure | Job retries, no duplicate documents |
| D3 | Retry from admin after failure | Document eventually created once |
| D4 | Duplicate job run for same payment | Still only one document record |

## E. Public roster

| ID | Scenario | Expected result |
|---|---|---|
| E1 | Published player with no visibility toggles | Display name only |
| E2 | Character toggle on | Character appears |
| E3 | Faction toggle on | Faction appears |
| E4 | Paid player | Paid status still hidden publicly |
| E5 | Unpublished player | No public entry appears |

## F. Ops / deployment

| ID | Scenario | Expected result |
|---|---|---|
| F1 | Web container starts | Health endpoint live |
| F2 | Worker container starts | Jobs picked up successfully |
| F3 | `/health/ready/` with DB down | Non-200 readiness |
| F4 | Logs emitted | Structured logs available |
| F5 | Secrets absent | App fails safely and clearly |
| F6 | Sandbox E2E | Full application -> approval -> payment -> document flow passes |
