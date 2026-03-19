from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 3
OLD_BODY = (
    "Arduino sends Digital Output signals using its DIGITAL Pins.\n\n"
    "Digital output sends only two states to components: HIGH (ON) or LOW (OFF).\n\n"
    "This lets Arduino control ***components with ON / OFF input*** such as LEDs or motors."
)
NEW_BODY = (
    "The DIGITAL pins also send output to the part components in only two states: HIGH (ON) or LOW (OFF).\n\n"
    "On Arduino, DIGITAL pins 2-13 are also used to ***send output to part components with two states*** "
    "such as LEDs or motors"
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
        ("levels", "0153_capitalize_digital_input_intro_first_word"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
