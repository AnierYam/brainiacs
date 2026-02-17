from django.db import migrations
from django.utils import timezone


def mark_legacy_accounts_verified(apps, schema_editor):
    ActivationCode = apps.get_model("landing", "ActivationCode")
    ActivationCode.objects.filter(
        user__isnull=False,
        email_verified_at__isnull=True,
        email_verification_sent_at__isnull=True,
        email_verification_code="",
    ).update(email_verified_at=timezone.now())


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0003_activationcode_email_verification_code_and_more"),
    ]

    operations = [
        migrations.RunPython(mark_legacy_accounts_verified, migrations.RunPython.noop),
    ]
