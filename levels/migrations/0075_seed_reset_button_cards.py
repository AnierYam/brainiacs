from copy import deepcopy
from django.db import migrations


def seed_reset_button_cards(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    reset_lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Reset Button").first()
    if not reset_lesson:
        return

    source_lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - The Brain Chip").first()
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
            lesson=reset_lesson,
            order=card.order,
            defaults=defaults,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0074_add_brain_chip_quiz_card"),
    ]

    operations = [
        migrations.RunPython(seed_reset_button_cards),
    ]
