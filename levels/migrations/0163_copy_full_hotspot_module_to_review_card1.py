from copy import deepcopy

from django.db import migrations


SOURCE_LESSON_TITLE = "Mission 2 Lesson 1 - USB Power Port"
SOURCE_CARD_ORDER = 2
TARGET_LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Board Quiz"
TARGET_CARD_ORDER = 1
OLD_HOTSPOTS = [
    {
        "id": "usb-port",
        "label": "USB Port",
        "bounds": {"left": 0.6, "top": 22.1, "width": 21.9, "height": 22.1},
    },
    {
        "id": "barrel-jack",
        "label": "Power Connector",
        "bounds": {"left": 3.85, "top": 74.26, "width": 20.52, "height": 22.65},
    },
    {
        "id": "reset-button",
        "label": "Reset Button",
        "bounds": {"left": 10.41, "top": 2.61, "width": 13.53, "height": 14.99},
    },
    {
        "id": "digital-pins",
        "label": "Digital Pins",
        "bounds": {"left": 45.35, "top": 1.5, "width": 50.2, "height": 17.1},
    },
    {
        "id": "l-led",
        "label": "L LED",
        "bounds": {"left": 40.4, "top": 20.2, "width": 8.6, "height": 5.7},
    },
    {
        "id": "tx-rx",
        "label": "TX/RX Lights",
        "bounds": {"left": 39.1, "top": 29.1, "width": 9.9, "height": 10.7},
    },
    {
        "id": "microcontroller",
        "label": "Microcontroller",
        "bounds": {"left": 44.6, "top": 61.0, "width": 51.2, "height": 18.65},
    },
    {
        "id": "analog-in",
        "label": "Analog IN Pins",
        "bounds": {"left": 72.9, "top": 80.88, "width": 22.9, "height": 17.64},
    },
]


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    source_lesson = Lesson.objects.filter(title=SOURCE_LESSON_TITLE).first()
    target_lesson = Lesson.objects.filter(title=TARGET_LESSON_TITLE).first()
    if not source_lesson or not target_lesson:
        return

    source_card = LessonCard.objects.filter(
        lesson=source_lesson,
        order=SOURCE_CARD_ORDER,
    ).first()
    target_card = LessonCard.objects.filter(
        lesson=target_lesson,
        order=TARGET_CARD_ORDER,
        card_type="quiz",
    ).first()
    if not source_card or not target_card:
        return

    source_payload = deepcopy(source_card.action_payload or {})
    source_hotspots = source_payload.get("hotspots")
    if not isinstance(source_hotspots, list) or not source_hotspots:
        return

    target_payload = deepcopy(target_card.action_payload or {})
    target_payload["hotspots"] = deepcopy(source_hotspots)
    if source_payload.get("alt"):
        target_payload["alt"] = source_payload["alt"]
    if "overlay_image" in source_payload:
        target_payload["overlay_image"] = deepcopy(source_payload["overlay_image"])
    else:
        target_payload.pop("overlay_image", None)

    target_card.action_payload = target_payload
    target_card.save(update_fields=["action_payload"])


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    target_lesson = Lesson.objects.filter(title=TARGET_LESSON_TITLE).first()
    if not target_lesson:
        return

    target_card = LessonCard.objects.filter(
        lesson=target_lesson,
        order=TARGET_CARD_ORDER,
        card_type="quiz",
    ).first()
    if not target_card:
        return

    target_payload = deepcopy(target_card.action_payload or {})
    target_payload["hotspots"] = deepcopy(OLD_HOTSPOTS)
    target_payload.pop("overlay_image", None)
    target_card.action_payload = target_payload
    target_card.save(update_fields=["action_payload"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0162_enable_selection_error_process_for_review_card4"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
