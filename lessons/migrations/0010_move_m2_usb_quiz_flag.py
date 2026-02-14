from django.db import migrations


PARENT_SLUG = "mission-2-arduino-board"


def apply_forward(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.filter(parent_slug=PARENT_SLUG, slug="power-input").update(
        has_quiz=False,
        xp_on_quiz_correct=0,
    )
    Step.objects.filter(parent_slug=PARENT_SLUG, slug="usb-input").update(
        has_quiz=True,
        xp_on_quiz_correct=15,
    )


def apply_reverse(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.filter(parent_slug=PARENT_SLUG, slug="power-input").update(
        has_quiz=True,
        xp_on_quiz_correct=15,
    )
    Step.objects.filter(parent_slug=PARENT_SLUG, slug="usb-input").update(
        has_quiz=True,
        xp_on_quiz_correct=15,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0009_reorder_m2_lesson1_units"),
    ]

    operations = [
        migrations.RunPython(apply_forward, apply_reverse),
    ]
