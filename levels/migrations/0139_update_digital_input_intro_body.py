from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 1
OLD_BODY = (
    "Digital input reads only two states: HIGH or LOW.\n\n"
    "On Arduino, DIGITAL pins (0-13) are used to read ***controllers with two states*** "
    "like push buttons or tilt sensors."
)
NEW_BODY = (
    "Digital input reads only two states: High (ON) or LOW (OFF).\n\n"
    "On Arduino, DIGITAL pins (2-13) are used to read *controllers with two states* "
    "HIGH / LOW like push buttons or ON / OFF switches."
)


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER).first()
    if not card:
        return

    card.body = NEW_BODY
    card.save(update_fields=["body"])


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER).first()
    if not card:
        return

    card.body = OLD_BODY
    card.save(update_fields=["body"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0138_update_digital_input_card_title"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
