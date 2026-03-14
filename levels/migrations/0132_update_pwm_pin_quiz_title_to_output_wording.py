from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
CARD_ORDER = 5
OLD_TITLE = "Which pins can OUTPUT ANALOG-Like SIGNAL?"
NEW_TITLE = "Which pins can give ANALOG-Like OUTPUT?"


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
        ("levels", "0131_update_pwm_pin_quiz_title"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
