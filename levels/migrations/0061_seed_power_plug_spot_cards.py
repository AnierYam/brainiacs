from copy import deepcopy
from django.db import migrations


def seed_power_plug_spot_cards(apps, schema_editor):
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

    power_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1 - Power Plug Spot",
        defaults={"order": 3},
    )

    usb_lesson = Lesson.objects.filter(
        system=system,
        title="Mission 2 Lesson 1 - USB Power Port",
    ).first()

    if usb_lesson:
        usb_cards = list(LessonCard.objects.filter(lesson=usb_lesson).order_by("order")[:2])
        for card in usb_cards:
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
                lesson=power_lesson,
                order=card.order,
                defaults=defaults,
            )
        return

    def blank_defaults():
        return {
            "title": "",
            "body": "",
            "image_url": "",
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "",
            "action_payload": {},
            "starter_code": "",
        }

    card_one = blank_defaults()
    card_one.update(
        {
            "card_type": "intro",
            "title": "Power Plug Spot",
            "body": "Lesson content coming soon.",
        }
    )
    LessonCard.objects.update_or_create(
        lesson=power_lesson,
        order=1,
        defaults=card_one,
    )

    card_two = blank_defaults()
    card_two.update(
        {
            "card_type": "action",
            "title": "Find the Power Plug Spot",
            "body": "Click the power plug spot on the Arduino board to reveal it.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "action_label": "I found the power plug spot",
            "action_payload": {
                "type": "image-hotspot",
                "target": "power-jack",
                "prompt": "Click the power plug spot on the board.",
                "alt": "Arduino Uno board",
                "bounds": {"left": 0.6, "top": 22.6, "width": 20.5, "height": 20.5},
                "success_message": "You found the power plug spot!",
                "fail_message": "Not quite. Try again.",
            },
        }
    )
    LessonCard.objects.update_or_create(
        lesson=power_lesson,
        order=2,
        defaults=card_two,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0060_clear_usb_power_port_card2_prompt"),
    ]

    operations = [
        migrations.RunPython(seed_power_plug_spot_cards),
    ]
