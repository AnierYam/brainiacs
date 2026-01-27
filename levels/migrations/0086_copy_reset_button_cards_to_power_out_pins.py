from copy import deepcopy
from django.db import migrations


def copy_reset_button_cards_to_power_out_pins(apps, schema_editor):
    Level = apps.get_model("levels", "Level")
    System = apps.get_model("levels", "System")
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    level = Level.objects.filter(number=1).first()
    if not level:
        return

    system = System.objects.filter(level=level, title="Mission 2: Pedro's Brain").first()
    if not system:
        return

    source_lesson = Lesson.objects.filter(
        system=system,
        title="Mission 2 Lesson 1 - Reset Button",
    ).first()
    if not source_lesson:
        return

    dest_lesson = Lesson.objects.filter(
        system=system,
        title="Mission 2 Lesson 1 - Power Out Pins",
    ).first()
    if not dest_lesson:
        return

    LessonCard.objects.filter(lesson=dest_lesson).delete()

    for card in LessonCard.objects.filter(lesson=source_lesson).order_by("order"):
        LessonCard.objects.create(
            lesson=dest_lesson,
            order=card.order,
            card_type=card.card_type,
            title=card.title,
            body=card.body,
            image_url=card.image_url,
            youtube_id=card.youtube_id,
            question=card.question,
            choice_a=card.choice_a,
            choice_b=card.choice_b,
            choice_c=card.choice_c,
            correct_choice=card.correct_choice,
            explanation=card.explanation,
            action_label=card.action_label,
            action_payload=deepcopy(card.action_payload),
            starter_code=card.starter_code,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0085_copy_checkpoint_cards_to_power_out_pins"),
    ]

    operations = [
        migrations.RunPython(copy_reset_button_cards_to_power_out_pins),
    ]
