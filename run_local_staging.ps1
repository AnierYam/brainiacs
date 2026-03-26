param(
    [int]$Port = 8001,
    [switch]$SkipMigrate,
    [switch]$NoServe
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$dbPath = Join-Path $repoRoot "db.staging.sqlite3"
$dbUriPath = $dbPath -replace "\\", "/"

Push-Location $repoRoot

try {
    $env:DJANGO_DEBUG = "False"
    $env:DJANGO_LOCAL_STAGING = "True"
    $env:ALLOWED_HOSTS = "127.0.0.1,localhost"
    $env:DJANGO_CSRF_TRUSTED_ORIGINS = "http://127.0.0.1:$Port,http://localhost:$Port"
    $env:SITE_URL = "http://127.0.0.1:$Port"
    $env:DATABASE_URL = "sqlite:///$dbUriPath"
    $env:EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    $env:DJANGO_SECURE_SSL_REDIRECT = "False"
    $env:DJANGO_USE_X_FORWARDED_HOST = "False"

    Write-Host "Starting Brainiacs local staging environment"
    Write-Host "URL: http://127.0.0.1:$Port/"
    Write-Host "Database: $dbPath"

    if (-not $SkipMigrate) {
        python manage.py migrate --noinput
        if ($LASTEXITCODE -ne 0) {
            exit $LASTEXITCODE
        }
    }

    if ($NoServe) {
        exit 0
    }

    python manage.py runserver --insecure "127.0.0.1:$Port"
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
