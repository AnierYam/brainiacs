from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
CARD_ORDER = 5

OLD_OPTIONS = [
    {"key": "13", "label": "13", "left": 47.0, "is_correct": False},
    {"key": "12", "label": "12", "left": 51.0, "is_correct": False},
    {"key": "11", "label": "11", "left": 55.0, "is_correct": True},
    {"key": "10", "label": "10", "left": 59.0, "is_correct": True},
    {"key": "9", "label": "9", "left": 63.0, "is_correct": True},
    {"key": "8", "label": "8", "left": 67.0, "is_correct": False},
    {"key": "7", "label": "7", "left": 71.5, "is_correct": False},
    {"key": "6", "label": "6", "left": 75.0, "is_correct": True},
    {"key": "5", "label": "5", "left": 78.5, "is_correct": True},
    {"key": "4", "label": "4", "left": 82.0, "is_correct": False},
    {"key": "3", "label": "3", "left": 85.5, "is_correct": True},
    {"key": "2", "label": "2", "left": 89.0, "is_correct": False},
]

NEW_OPTIONS = [
    {"key": "13", "label": "13", "left": 8.5, "is_correct": False},
    {"key": "12", "label": "12", "left": 16.0, "is_correct": False},
    {"key": "11", "label": "11", "left": 23.5, "is_correct": True},
    {"key": "10", "label": "10", "left": 31.0, "is_correct": True},
    {"key": "9", "label": "9", "left": 38.5, "is_correct": True},
    {"key": "8", "label": "8", "left": 46.0, "is_correct": False},
    {"key": "7", "label": "7", "left": 55.0, "is_correct": False},
    {"key": "6", "label": "6", "left": 62.5, "is_correct": True},
    {"key": "5", "label": "5", "left": 70.0, "is_correct": True},
    {"key": "4", "label": "4", "left": 77.5, "is_correct": False},
    {"key": "3", "label": "3", "left": 85.0, "is_correct": True},
    {"key": "2", "label": "2", "left": 92.5, "is_correct": False},
]


def apply_payload_update(payload, options, min_width, max_width):
    payload["options"] = options
    payload["board_min_width"] = min_width
    payload["board_max_width"] = max_width
    return payload


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER).first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    card.action_payload = apply_payload_update(payload, NEW_OPTIONS, 900, 980)
    card.save(update_fields=["action_payload"])


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER).first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    card.action_payload = apply_payload_update(payload, OLD_OPTIONS, 760, 820)
    card.save(update_fields=["action_payload"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0128_remove_pins_1_and_0_from_pwm_quiz"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
