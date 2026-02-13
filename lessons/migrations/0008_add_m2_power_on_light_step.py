from django.db import migrations
from django.db.models import F


PARENT_SLUG = "mission-2-arduino-board"
STEP_SLUG = "on-led"
STEP_ORDER = 4


def add_power_on_light_step(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    existing = Step.objects.filter(parent_slug=PARENT_SLUG, slug=STEP_SLUG).first()

    if existing:
        old_order = existing.order
        if old_order > STEP_ORDER:
            Step.objects.filter(
                parent_slug=PARENT_SLUG,
                order__gte=STEP_ORDER,
                order__lt=old_order,
            ).exclude(pk=existing.pk).update(order=F("order") + 1)
        elif old_order < STEP_ORDER:
            Step.objects.filter(
                parent_slug=PARENT_SLUG,
                order__gt=old_order,
                order__lte=STEP_ORDER,
            ).exclude(pk=existing.pk).update(order=F("order") - 1)

        existing.title = "Power On Light"
        existing.order = STEP_ORDER
        existing.content_mode = "cards"
        existing.has_quiz = True
        existing.xp_on_complete = 10
        existing.xp_on_quiz_correct = 15
        existing.save(
            update_fields=[
                "title",
                "order",
                "content_mode",
                "has_quiz",
                "xp_on_complete",
                "xp_on_quiz_correct",
            ]
        )
        return

    Step.objects.filter(parent_slug=PARENT_SLUG, order__gte=STEP_ORDER).update(order=F("order") + 1)
    Step.objects.create(
        slug=STEP_SLUG,
        title="Power On Light",
        parent_slug=PARENT_SLUG,
        order=STEP_ORDER,
        content_mode="cards",
        has_quiz=True,
        xp_on_complete=10,
        xp_on_quiz_correct=15,
    )


def remove_power_on_light_step(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    step = Step.objects.filter(parent_slug=PARENT_SLUG, slug=STEP_SLUG).first()
    if not step:
        return

    removed_order = step.order
    step.delete()
    Step.objects.filter(parent_slug=PARENT_SLUG, order__gt=removed_order).update(order=F("order") - 1)


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0007_add_m2_checkpoint_quiz_step"),
    ]

    operations = [
        migrations.RunPython(add_power_on_light_step, remove_power_on_light_step),
    ]
