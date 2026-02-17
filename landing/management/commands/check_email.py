from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Validate email settings and optionally send a test email."

    def add_arguments(self, parser):
        parser.add_argument(
            "--to",
            dest="to_email",
            help="Recipient address for a test email.",
        )

    def handle(self, *args, **options):
        self.stdout.write(f"DEBUG={settings.DEBUG}")
        self.stdout.write(f"EMAIL_BACKEND={settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST={settings.EMAIL_HOST!r}")
        self.stdout.write(f"EMAIL_PORT={settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_HOST_USER={settings.EMAIL_HOST_USER!r}")
        self.stdout.write(f"EMAIL_USE_TLS={settings.EMAIL_USE_TLS}")
        self.stdout.write(f"EMAIL_TIMEOUT={settings.EMAIL_TIMEOUT}")
        self.stdout.write(f"DEFAULT_FROM_EMAIL={settings.DEFAULT_FROM_EMAIL!r}")
        self.stdout.write(
            f"BRAINIACS_OUTBOUND_FROM_EMAIL={settings.BRAINIACS_OUTBOUND_FROM_EMAIL!r}"
        )
        if settings.EMAIL_BACKEND == "django.core.mail.backends.console.EmailBackend":
            self.stdout.write(
                self.style.WARNING(
                    "Console backend active: this writes email to logs, not inboxes."
                )
            )

        to_email = options.get("to_email")
        if not to_email:
            self.stdout.write(self.style.WARNING("No --to provided; config only."))
            return

        try:
            sent = send_mail(
                subject="Brainiacs email test",
                message="This is a Brainiacs SMTP test email.",
                from_email=settings.BRAINIACS_OUTBOUND_FROM_EMAIL,
                recipient_list=[to_email],
                fail_silently=False,
            )
        except Exception as exc:
            raise CommandError(f"Email send failed: {exc}") from exc

        if sent == 1:
            self.stdout.write(
                self.style.SUCCESS(f"Test email sent successfully to {to_email}.")
            )
        else:
            raise CommandError(f"Email send returned unexpected count: {sent}")
