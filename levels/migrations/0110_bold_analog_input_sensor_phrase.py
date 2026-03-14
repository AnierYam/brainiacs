from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
CARD_ORDER = 1
OLD_BODY = (
    "Analog input reads a range of values instead of just ON or OFF.\n\n"
    "On Arduino, analog pins (A0-A5) are used to read *sensors that change values* like Joystick, Potentiometer."
)
NEW_BODY = (
    "Analog input reads a range of values instead of just ON or OFF.\n\n"
    "On Arduino, analog pins (A0-A5) are used to read ***controllers that change values*** like Joystick, Potentiometer."
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
        ("levels", "0109_remove_sound_sensor_from_analog_input_card"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
