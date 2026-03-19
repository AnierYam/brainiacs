from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 1
OLD_BODY = (
    "the DIGITAL pins take input from the controller in only two states: HIGH (ON) or LOW (OFF)\n\n"
    "On Arduino, DIGITAL pins 2-13 are used to ***read input from controllers with two states*** "
    "like push buttons or switches"
)
NEW_BODY = (
    "The DIGITAL pins take input from the controller in only two states: HIGH (ON) or LOW (OFF)\n\n"
    "On Arduino, DIGITAL pins 2-13 are used to ***read input from controllers with two states*** "
    "like push buttons or switches"
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
        ("levels", "0152_make_digital_input_phrase_bold_and_italic"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
