from django.db import migrations


DEMO_CODE = "BRAINIACS!@2026.,;"


def create_demo_activation_code(apps, schema_editor):
    activation_code_model = apps.get_model("landing", "ActivationCode")
    activation_code_model.objects.get_or_create(code=DEMO_CODE)


def remove_demo_activation_code(apps, schema_editor):
    activation_code_model = apps.get_model("landing", "ActivationCode")
    activation_code_model.objects.filter(code=DEMO_CODE, user__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_demo_activation_code,
            reverse_code=remove_demo_activation_code,
        ),
    ]
