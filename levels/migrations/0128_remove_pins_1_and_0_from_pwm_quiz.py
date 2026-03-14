from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
CARD_ORDER = 5


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
    options = list(payload.get("options") or [])
    payload["options"] = [
        option
        for option in options
        if str(option.get("key")) not in {"1", "0"}
    ]
    card.action_payload = payload
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
    options = list(payload.get("options") or [])
    existing_keys = {str(option.get("key")) for option in options}
    if "1" not in existing_keys:
        options.append({"key": "1", "label": "1", "left": 92.5, "is_correct": False})
    if "0" not in existing_keys:
        options.append({"key": "0", "label": "0", "left": 96.0, "is_correct": False})
    payload["options"] = sorted(options, key=lambda option: float(option.get("left", 0)))
    card.action_payload = payload
    card.save(update_fields=["action_payload"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0127_convert_card5_to_pwm_pin_quiz"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
