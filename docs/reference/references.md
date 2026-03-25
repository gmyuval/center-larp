# Reference notes

All external references below were checked on 2026-03-25.

## R1 — Django 5.2
- Django 5.2 release notes (LTS, Python compatibility): https://docs.djangoproject.com/en/5.2/releases/5.2/
- Django FAQ: installation / supported Python versions and DB recommendations: https://docs.djangoproject.com/en/5.2/faq/install/

Notes used in this package:
- Django 5.2 is an LTS release.
- Django 5.2 supports Python 3.10–3.14 as of 5.2.8.
- PostgreSQL is the recommended production database.

## R2 — Cardcom Low Profile
- Step 1+2 - Creating a payment page & sending a request to retrieve transaction details (Iframe/Redirect): https://cardcomapi.zendesk.com/hc/he/articles/28448202810514-Step-1-2-Creating-a-payment-page-sending-a-request-to-retrieve-transaction-details-Iframe-Redirect

Notes used in this package:
- Web payment pages are created through `POST /api/v11/LowProfile/Create`.
- The merchant should pass an internal identifier through `ReturnValue`.
- Redirect/success pages are not sufficient as payment truth.
- The server should verify via `GET /api/v11/LowProfile/GetLpResult`.
- A public external callback/redirect URL is required.
- Cardcom retries webhook delivery if the merchant does not return HTTP 200.

## R3 — Cardcom direct interface warning
- Step 3 - Token Charging / Frame Capture / Direct Interface Credit Card Charging (Do Transaction): https://cardcomapi.zendesk.com/hc/he/articles/28452352778770-Step-3-Token-Charging-Frame-Capture-Direct-Interface-Credit-Card-Charging-Do-Transaction

Notes used in this package:
- Direct interface is not intended for WEB sites.
- Low Profile should be used for website payment flows.

## R4 — Morning API access
- API overview: https://www.greeninvoice.co.il/help-center/api/
- API key creation: https://www.greeninvoice.co.il/help-center/generating-api-key/

Notes used in this package:
- API access is available on Best and up.
- The API key secret is shown only once at creation time.
- Morning provides a sandbox flow for testing integrations.

## R5 — Morning webhooks
- Webhook configuration: https://www.greeninvoice.co.il/help-center/creating-webhook/

Notes used in this package:
- Webhooks are available on Best and up.
- Webhook callback URLs must start with `https`.
- A secret can be configured.
- If no response is received within 6 seconds, Morning retries deliveries for up to 24 hours.

## R6 — Morning document types
- Webhook - document/created: https://www.greeninvoice.co.il/help-center/webhook-document-created/
- Document type overview: https://www.greeninvoice.co.il/help-center/all-documents-types/

Notes used in this package:
- Relevant document types include 305 (tax invoice), 320 (tax invoice / receipt), and 400 (receipt).
- The document/created event payload includes document id, number, recipient, items, transactions, and download links.

## R7 — Morning email sending behavior
- Send document by email: https://www.greeninvoice.co.il/help-center/send-by-email/

Notes used in this package:
- Morning supports sending generated documents to customers by email from the system.
- Automatic sending can be configured for saved clients.

## R8 — Landing page reference
- User-supplied HTML reference: `reference/foreign_gates_v4.html`

Notes used in this package:
- The production landing page should preserve the overall visual language and section structure of the supplied file while replacing the CTA target with the application form.
