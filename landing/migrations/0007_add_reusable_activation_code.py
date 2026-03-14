from django.db import migrations, models


PERMANENT_CODE = "BRAINIACS!@2026.,;"


def create_permanent_activation_code(apps, schema_editor):
    activation_code_model = apps.get_model("landing", "ActivationCode")
    activation_code, _ = activation_code_model.objects.get_or_create(
        code=PERMANENT_CODE,
        defaults={"is_reusable": True},
    )
    if not activation_code.is_reusable:
        activation_code.is_reusable = True
        activation_code.save(update_fields=["is_reusable"])


def remove_permanent_activation_code(apps, schema_editor):
    activation_code_model = apps.get_model("landing", "ActivationCode")
    activation_code_model.objects.filter(
        code=PERMANENT_CODE,
        is_reusable=True,
        user__isnull=True,
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0006_seed_otp001_activation_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="activationcode",
            name="is_reusable",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            create_permanent_activation_code,
            reverse_code=remove_permanent_activation_code,
        ),
    ]
