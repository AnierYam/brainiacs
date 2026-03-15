from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 2
OLD_TITLE = "FIND the Digital input pins (DIGITAL (PWM ~) )"
NEW_TITLE = "FIND the Digital Input pins (DIGITAL (PWM ~) )"


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
        ("levels", "0143_update_digital_input_action_title_again"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
