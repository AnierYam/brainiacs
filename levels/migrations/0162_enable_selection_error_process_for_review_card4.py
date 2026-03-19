from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Board Quiz"
CARD_ORDER = 4


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER, card_type="quiz").first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    payload["selection_error_process"] = True
    card.action_payload = payload
    card.save(update_fields=["action_payload"])


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER, card_type="quiz").first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    payload.pop("selection_error_process", None)
    card.action_payload = payload
    card.save(update_fields=["action_payload"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0161_add_lesson1_review_cards"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
