from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 1
OLD_TITLE = "What is Digital Input (DIGITAL IN)"
NEW_TITLE = "What is Digital Input (DIGITAL (PWM ~) )"


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER).first()
    if not card:
        return

    card.title = NEW_TITLE
    card.save(update_fields=["title"])


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER).first()
    if not card:
        return

    card.title = OLD_TITLE
    card.save(update_fields=["title"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0137_copy_analog_io_flow_to_digital_io_lesson"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
