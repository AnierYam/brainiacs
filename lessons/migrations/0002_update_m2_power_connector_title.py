from django.db import migrations


def update_m2_power_connector_title(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.filter(
        parent_slug="mission-2-arduino-board",
        slug="power-input",
    ).update(title="Power Connector")


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(update_m2_power_connector_title),
    ]
