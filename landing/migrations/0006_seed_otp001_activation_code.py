from django.db import migrations


ONE_TIME_CODE = "OTP001"


def create_otp001_activation_code(apps, schema_editor):
    activation_code_model = apps.get_model("landing", "ActivationCode")
    activation_code_model.objects.get_or_create(code=ONE_TIME_CODE)


def remove_otp001_activation_code(apps, schema_editor):
    activation_code_model = apps.get_model("landing", "ActivationCode")
    activation_code_model.objects.filter(code=ONE_TIME_CODE, user__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0005_logindevice"),
    ]

    operations = [
        migrations.RunPython(
            create_otp001_activation_code,
            reverse_code=remove_otp001_activation_code,
        ),
    ]
