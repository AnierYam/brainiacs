from copy import deepcopy
from django.db import migrations


def seed_brain_chip_cards(apps, schema_editor):
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

    brain_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1 - The Brain Chip",
        defaults={"order": 4},
    )

    source_lesson = Lesson.objects.filter(
        system=system,
        title="Mission 2 Lesson 1 - Power Connector",
    ).first()

    if not source_lesson:
        source_lesson = Lesson.objects.filter(
            system=system,
            title="Mission 2 Lesson 1 - USB Power Port",
        ).first()

    if not source_lesson:
        return

    source_cards = list(LessonCard.objects.filter(lesson=source_lesson).order_by("order"))
    for card in source_cards:
        defaults = {
            "card_type": card.card_type,
            "title": card.title,
            "body": card.body,
            "image_url": card.image_url,
            "youtube_id": card.youtube_id,
            "question": card.question,
            "choice_a": card.choice_a,
            "choice_b": card.choice_b,
            "choice_c": card.choice_c,
            "correct_choice": card.correct_choice,
            "explanation": card.explanation,
            "action_label": card.action_label,
            "action_payload": deepcopy(card.action_payload or {}),
            "starter_code": card.starter_code,
        }
        LessonCard.objects.update_or_create(
            lesson=brain_lesson,
            order=card.order,
            defaults=defaults,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0069_remove_pinout_reward_card"),
    ]

    operations = [
        migrations.RunPython(seed_brain_chip_cards),
    ]
