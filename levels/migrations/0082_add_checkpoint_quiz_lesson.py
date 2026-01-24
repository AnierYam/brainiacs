from copy import deepcopy
from django.db import migrations


def add_checkpoint_quiz_lesson(apps, schema_editor):
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

    checkpoint_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1 - Checkpoint Quiz",
        defaults={"order": 6},
    )

    source_lesson = Lesson.objects.filter(
        system=system,
        title="Mission 2 Lesson 1 - USB Power Port",
    ).first()
    source_card = None
    if source_lesson:
        source_card = (
            LessonCard.objects.filter(lesson=source_lesson, card_type="action")
            .order_by("order")
            .first()
        )

    payload = deepcopy(source_card.action_payload) if source_card else {}
    payload.setdefault("type", "sequence-hotspot")
    payload.pop("target", None)
    payload.pop("bounds", None)
    payload.pop("label", None)
    payload["sequence_title"] = "Click in this order:"
    payload["sequence_pool"] = [
        "usb-port",
        "power-jack",
        "microcontroller",
        "reset-button",
    ]
    payload["success_message"] = "Nice work! You completed the sequence."
    payload["fail_message"] = "Not quite. Try the sequence again from the start."
    payload["show_prompt"] = False

    LessonCard.objects.update_or_create(
        lesson=checkpoint_lesson,
        order=1,
        defaults={
            "card_type": "action",
            "title": "Checkpoint Quiz",
            "body": "Click the parts in the order shown.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "action_label": "",
            "action_payload": payload,
        },
    )

    LessonCard.objects.update_or_create(
        lesson=checkpoint_lesson,
        order=2,
        defaults={
            "card_type": "intro",
            "title": "Checkpoint Quiz",
            "body": "Card 2 content coming next.",
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0081_add_reset_button_quiz_card"),
    ]

    operations = [
        migrations.RunPython(add_checkpoint_quiz_lesson),
    ]
