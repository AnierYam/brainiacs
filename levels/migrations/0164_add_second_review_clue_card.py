from copy import deepcopy

from django.db import migrations


SOURCE_LESSON_TITLE = "Mission 2 Lesson 1 - USB Power Port"
SOURCE_CARD_ORDER = 2
TARGET_LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Board Quiz"
TARGET_CARD_ORDER = 9
BOARD_IMAGE = "/static/lessons/mission2/arduino_board.png"

CLUES = [
    {"target": "digital-pins", "text": "I can read or give HIGH and LOW."},
    {"target": "analog-in", "text": "I read changing values from sensors."},
    {"target": "power-header", "text": "I hold pins such as 5V and GND."},
    {"target": "on-led", "text": "I stay lit when the board has power."},
    {"target": "tx-rx", "text": "We blink when data is sent or received."},
    {"target": "l-led", "text": "I am the built-in light linked to pin 13."},
]


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    source_lesson = Lesson.objects.filter(title=SOURCE_LESSON_TITLE).first()
    target_lesson = Lesson.objects.filter(title=TARGET_LESSON_TITLE).first()
    if not source_lesson or not target_lesson:
        return

    source_card = LessonCard.objects.filter(lesson=source_lesson, order=SOURCE_CARD_ORDER).first()
    if not source_card:
        return

    source_payload = deepcopy(source_card.action_payload or {})
    hotspots = deepcopy(source_payload.get("hotspots") or [])
    if not hotspots:
        return

    payload = {
        "quiz_type": "clue-hotspot",
        "alt": source_payload.get("alt") or "Arduino Uno board",
        "hotspots": hotspots,
        "clues": deepcopy(CLUES),
        "progress_feedback": "Correct. Move to the next clue.",
        "success_message": "Correct! You found the rest of the board features from their clues.",
        "fail_message": "Not quite. Stay on this clue and try again.",
        "completed_prompt": "Every extra board clue is solved.",
    }
    if "overlay_image" in source_payload:
        payload["overlay_image"] = deepcopy(source_payload["overlay_image"])

    LessonCard.objects.update_or_create(
        lesson=target_lesson,
        order=TARGET_CARD_ORDER,
        defaults={
            "card_type": "quiz",
            "title": "More Board Clues",
            "body": "Use the next set of clues to find the remaining board features.",
            "image_url": source_card.image_url or BOARD_IMAGE,
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "",
            "action_payload": payload,
            "starter_code": "",
        },
    )


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    target_lesson = Lesson.objects.filter(title=TARGET_LESSON_TITLE).first()
    if not target_lesson:
        return

    LessonCard.objects.filter(
        lesson=target_lesson,
        order=TARGET_CARD_ORDER,
        card_type="quiz",
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0163_copy_full_hotspot_module_to_review_card1"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
