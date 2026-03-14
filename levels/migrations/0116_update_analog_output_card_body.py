from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
CARD_ORDER = 3
OLD_BODY = (
    "Arduino can create analog-like output from some DIGITAL pins.\n\n"
    "These pins are marked with a ~ symbol and use PWM (Pulse Width Modulation)."
)
NEW_BODY = (
    "Arduino can create analog output from the DIGITAL pins.\n\n"
    "These pins are marked with the ~ symbol."
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
        ("levels", "0115_capitalize_analog_output_title"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
