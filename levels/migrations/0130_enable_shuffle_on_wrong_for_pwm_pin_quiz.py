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
    payload["shuffle_on_wrong"] = True
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
    payload.pop("shuffle_on_wrong", None)
    card.action_payload = payload
    card.save(update_fields=["action_payload"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0129_spread_pwm_quiz_pins_for_touch"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
