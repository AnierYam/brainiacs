# Local Staging

Use this when you want a personal staging environment on your own machine before pushing to production.

## What it does

- Runs the site on `http://127.0.0.1:8001/`
- Uses a separate SQLite database: `db.staging.sqlite3`
- Uses production-like app settings:
  - `DJANGO_DEBUG=False`
  - `DJANGO_LOCAL_STAGING=True`
  - fixed `SITE_URL`
  - explicit `ALLOWED_HOSTS`
  - explicit `DJANGO_CSRF_TRUSTED_ORIGINS`
- Disables HTTPS-only cookie and manifest-static behavior that would otherwise break a local HTTP staging run
- Uses the console email backend so local staging does not require SMTP credentials

## Start local staging

From the repo root:

```powershell
.\run_local_staging.ps1
```

Then open:

```text
http://127.0.0.1:8001/
```

## Useful options

Start on a different port:

```powershell
.\run_local_staging.ps1 -Port 8010
```

Skip migrations:

```powershell
.\run_local_staging.ps1 -SkipMigrate
```

Run setup only, without starting the server:

```powershell
.\run_local_staging.ps1 -NoServe
```

## Notes

- This is personal/local only. It is not a public staging URL.
- Your normal local database `db.sqlite3` is left untouched.
- The staging database is ignored by Git because `*.sqlite3` is already in `.gitignore`.
