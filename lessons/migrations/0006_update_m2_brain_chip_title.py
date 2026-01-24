from django.db import migrations


def update_brain_chip_title(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.filter(
        parent_slug="mission-2-arduino-board",
        slug="microcontroller",
    ).update(title="🧠 The Brain Chip")


def revert_brain_chip_title(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.filter(
        parent_slug="mission-2-arduino-board",
        slug="microcontroller",
    ).update(title="🧠 Tiny Brain Chip")


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0005_stepreview"),
    ]

    operations = [
        migrations.RunPython(update_brain_chip_title, revert_brain_chip_title),
    ]
