from django.db import migrations
from django.db.models import F


def add_checkpoint_quiz_step(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    parent_slug = "mission-2-arduino-board"
    existing = Step.objects.filter(parent_slug=parent_slug, slug="checkpoint-quiz").first()
    if existing:
        return

    Step.objects.create(
        slug="checkpoint-quiz",
        title="🧩 Checkpoint Quiz",
        parent_slug=parent_slug,
        order=6,
        content_mode="cards",
        has_quiz=True,
        xp_on_complete=10,
        xp_on_quiz_correct=15,
    )

    Step.objects.filter(parent_slug=parent_slug, order__gte=6).exclude(slug="checkpoint-quiz").update(
        order=F("order") + 1
    )


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0006_update_m2_brain_chip_title"),
    ]

    operations = [
        migrations.RunPython(add_checkpoint_quiz_step),
    ]
