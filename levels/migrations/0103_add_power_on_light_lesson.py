import copy

from django.db import migrations
from django.db.models import F


SOURCE_LESSON_TITLE = "Mission 2 Lesson 1 - Power Connector"
TARGET_LESSON_TITLE = "Mission 2 Lesson 1 - Power On Light"


def add_power_on_light_lesson(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    source = Lesson.objects.filter(title=SOURCE_LESSON_TITLE).first()
    if not source:
        return

    desired_order = source.order + 1
    target = Lesson.objects.filter(title=TARGET_LESSON_TITLE).first()
    if not target:
        Lesson.objects.filter(system=source.system, order__gt=source.order).update(order=F("order") + 1)
        target = Lesson.objects.create(
            system=source.system,
            title=TARGET_LESSON_TITLE,
            video_link=source.video_link,
            image=source.image,
            order=desired_order,
        )
    else:
        update_fields = []
        if target.system_id != source.system_id:
            target.system_id = source.system_id
            update_fields.append("system")
        if target.order != desired_order:
            target.order = desired_order
            update_fields.append("order")
        if target.video_link != source.video_link:
            target.video_link = source.video_link
            update_fields.append("video_link")
        if target.image != source.image:
            target.image = source.image
            update_fields.append("image")
        if update_fields:
            target.save(update_fields=update_fields)

    source_cards = list(LessonCard.objects.filter(lesson=source).order_by("order"))
    if not source_cards:
        return

    for card in source_cards:
        LessonCard.objects.update_or_create(
            lesson=target,
            order=card.order,
            defaults={
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
                "action_payload": card.action_payload,
                "starter_code": card.starter_code,
            },
        )

    LessonCard.objects.filter(lesson=target).exclude(order__in=[1, 2, 3]).delete()

    LessonCard.objects.update_or_create(
        lesson=target,
        order=1,
        defaults={
            "card_type": "intro",
            "title": "What is the Power On Light",
            "body": (
                "The ON LED is the small light that tells you the Arduino has power.\n\n"
                "If this light is on, the board is receiving electricity and is ready to run code."
            ),
            "image_url": "/static/lessons/mission2/arduino_board.png",
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
        },
    )

    source_action_card = next((card for card in source_cards if card.order == 2), None)
    payload = copy.deepcopy(source_action_card.action_payload if source_action_card else {})
    if isinstance(payload, dict):
        payload["target"] = "on-led"
        payload["prompt"] = "Hover over the main parts to see them move, then click the ON LED."
        payload["success_message"] = "You found the ON LED!"
        payload["fail_message"] = "Not quite. Try again."

        hotspots = payload.get("hotspots")
        if isinstance(hotspots, list):
            for hotspot in hotspots:
                if not isinstance(hotspot, dict):
                    continue
                if hotspot.get("id") == "on-led":
                    hotspot["is_target"] = True
                    hotspot["label"] = "ON LED"
                else:
                    hotspot.pop("is_target", None)

    LessonCard.objects.update_or_create(
        lesson=target,
        order=2,
        defaults={
            "card_type": "action",
            "title": "Find the ON LED",
            "body": "Hover over the main parts to see them move, then click the ON LED.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the ON LED",
            "action_payload": payload if isinstance(payload, dict) else {},
            "starter_code": "",
        },
    )

    LessonCard.objects.update_or_create(
        lesson=target,
        order=3,
        defaults={
            "card_type": "quiz",
            "title": "Quick Check Power On Light",
            "body": "Choose one answer.",
            "image_url": "",
            "youtube_id": "",
            "question": "What does it mean when the ON LED is lit?",
            "choice_a": "The Arduino has power",
            "choice_b": "The reset button is pressed",
            "choice_c": "The USB cable is disconnected",
            "correct_choice": "A",
            "explanation": "Correct. The ON LED shows the board is powered.",
            "action_label": "",
            "action_payload": {},
            "starter_code": "",
        },
    )


def remove_power_on_light_lesson(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    target = Lesson.objects.filter(title=TARGET_LESSON_TITLE).first()
    if not target:
        return

    system_id = target.system_id
    removed_order = target.order

    LessonCard.objects.filter(lesson=target).delete()
    target.delete()

    Lesson.objects.filter(system_id=system_id, order__gt=removed_order).update(order=F("order") - 1)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0102_copy_power_out_pins_cards_to_digital_vs_analog"),
    ]

    operations = [
        migrations.RunPython(add_power_on_light_lesson, remove_power_on_light_lesson),
    ]
