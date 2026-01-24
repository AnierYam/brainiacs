from django.db import migrations


def update_m2_power_connector_title_with_emoji(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.filter(
        parent_slug="mission-2-arduino-board",
        slug="power-input",
    ).update(title="\u26A1 Power Connector")


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0002_update_m2_power_connector_title"),
    ]

    operations = [
        migrations.RunPython(update_m2_power_connector_title_with_emoji),
    ]
