# Email Setup (Render)

## Provider Modes
- `EMAIL_PROVIDER=smtp` (default): use your SMTP credentials (Gmail/app password or any SMTP provider).
- `EMAIL_PROVIDER=sendgrid` (or set `SENDGRID_API_KEY`): uses SendGrid SMTP defaults (`smtp.sendgrid.net`, user `apikey`).

## Required Env Vars (Render)
- `SITE_URL=https://brainiacs.academy`
- `DEFAULT_FROM_EMAIL=Brainiacs <no-reply@brainiacs.academy>`
- `BRAINIACS_OUTBOUND_FROM_EMAIL=<verified sender>`
- `BRAINIACS_SUPPORT_EMAIL=<support inbox>`

### SMTP (Gmail/other)
- `EMAIL_PROVIDER=smtp`
- `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
- `EMAIL_HOST=<smtp host>`
- `EMAIL_PORT=587`
- `EMAIL_USE_TLS=true`
- `EMAIL_HOST_USER=<smtp username>`
- `EMAIL_HOST_PASSWORD=<smtp password>`

### SendGrid (recommended)
- `EMAIL_PROVIDER=sendgrid`
- `SENDGRID_API_KEY=<sendgrid api key>`
- Optional overrides:
  - `EMAIL_HOST=smtp.sendgrid.net`
  - `EMAIL_PORT=587`
  - `EMAIL_HOST_USER=apikey`
  - `EMAIL_USE_TLS=true`

## Commands
- Config check + test send:
  - `python manage.py check_email --to you@example.com`
- Template-level test emails:
  - `python manage.py test_email --to you@example.com --type verification`
  - `python manage.py test_email --to you@example.com --type login`
  - `python manage.py test_email --to you@example.com --type kit`
  - `python manage.py test_email --to you@example.com --type admin`

## Manual Checklist
1. Create account via kit activation -> verification email arrives.
2. Login twice from same browser/device -> alert should trigger once.
3. Login from another browser/incognito -> alert should trigger.
4. Use resend verification on confirm page -> email arrives.

## Deliverability Note
For production deliverability, configure domain authentication (SPF + DKIM) on your sending domain (especially for SendGrid).

