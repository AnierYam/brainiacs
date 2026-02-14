from django.db import migrations


SOURCE_TITLE = "Mission 2 Lesson 1 - Power Connector"
DEST_TITLE = "Mission 2 Lesson 1 - USB Power Port"
QUIZ_ORDER = 3


def _move_quiz_card(apps, from_title, to_title):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    source_lesson = Lesson.objects.filter(title=from_title).first()
    dest_lesson = Lesson.objects.filter(title=to_title).first()
    if not source_lesson or not dest_lesson:
        return

    source_card = LessonCard.objects.filter(
        lesson=source_lesson,
        order=QUIZ_ORDER,
        card_type="quiz",
    ).first()
    if not source_card:
        source_card = LessonCard.objects.filter(
            lesson=source_lesson,
            card_type="quiz",
        ).order_by("order").first()
    if not source_card:
        return

    existing_dest = LessonCard.objects.filter(lesson=dest_lesson, order=QUIZ_ORDER).first()
    if existing_dest and existing_dest.id != source_card.id:
        existing_dest.delete()

    source_card.lesson = dest_lesson
    source_card.order = QUIZ_ORDER
    source_card.save(update_fields=["lesson", "order"])


def move_forward(apps, schema_editor):
    _move_quiz_card(apps, SOURCE_TITLE, DEST_TITLE)


def move_backward(apps, schema_editor):
    _move_quiz_card(apps, DEST_TITLE, SOURCE_TITLE)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0105_move_unit3_card4_to_digital_io"),
    ]

    operations = [
        migrations.RunPython(move_forward, move_backward),
    ]
