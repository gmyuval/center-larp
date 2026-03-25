# Deployment checklist

## Before first staging deployment
- [ ] Django project builds in Docker
- [ ] PostgreSQL connection works
- [ ] migrations run successfully
- [ ] static files collect successfully
- [ ] `/health/live/` and `/health/ready/` exist
- [ ] GM admin user created
- [ ] event YAML and form YAML committed
- [ ] landing page loads from template
- [ ] email backend configured for non-prod

## Before Cardcom sandbox test
- [ ] Cardcom sandbox / test credentials set
- [ ] public staging URL exists over HTTPS
- [ ] Cardcom callback URL points to staging webhook
- [ ] success / failure return URLs point to staging
- [ ] outbound access from worker to Cardcom allowed

## Before Morning sandbox test
- [ ] Morning sandbox account exists
- [ ] sandbox Best flow completed if required for API access
- [ ] Morning sandbox API key created
- [ ] secret stored securely
- [ ] outbound access from worker to Morning allowed
- [ ] final document type confirmed for testing

## Before production cutover
- [ ] `center.larp.co.il` DNS points to production reverse proxy
- [ ] TLS certificate active
- [ ] production DB available and backed up
- [ ] production secrets set
- [ ] production Cardcom webhook URL configured
- [ ] production Morning API key configured
- [ ] GM notification mailbox configured
- [ ] applicant confirmation email tested
- [ ] payment link email tested
- [ ] Morning document email behavior tested
- [ ] worker deployed and running
- [ ] log aggregation / alerting connected
- [ ] smoke test passes on production domain

## Post-launch
- [ ] first real application submitted successfully
- [ ] first approval completed successfully
- [ ] first payment verified successfully
- [ ] first Morning document created successfully
- [ ] first public roster publish verified
- [ ] backup restore procedure documented
