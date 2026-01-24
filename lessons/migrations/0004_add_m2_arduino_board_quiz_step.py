from django.db import migrations


def add_m2_arduino_board_quiz_step(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.get_or_create(
        parent_slug="mission-2-arduino-board",
        slug="arduino-board-quiz",
        defaults={
            "title": "\U0001F4DD Arduino Board Quiz",
            "order": 9,
            "content_mode": "cards",
            "has_quiz": True,
            "xp_on_complete": 10,
            "xp_on_quiz_correct": 15,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0003_update_m2_power_connector_title_with_emoji"),
    ]

    operations = [
        migrations.RunPython(add_m2_arduino_board_quiz_step),
    ]
