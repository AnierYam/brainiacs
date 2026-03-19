from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 5
OLD_TITLE = "Which pins can give DIGITAL OUTPUT?"
OLD_BODY = "Choose true or false."
OLD_QUESTION = "The DIGITAL pins only give out Digital output."
OLD_EXPLANATION = "Correct! DIGITAL pins can be used as INPUT or OUTPUT."
OLD_ACTION_PAYLOAD = {
    "selection_error_process": True,
}
NEW_TITLE = "The DIGITAL pins only give out Digital output."
NEW_BODY = "Choose true or false."
NEW_QUESTION = ""
NEW_EXPLANATION = "Correct! DIGITAL pins can be used as INPUT or OUTPUT."
NEW_ACTION_PAYLOAD = {
    "selection_error_process": True,
    "question_display": "title",
    "selection_error_feedback": "Hint: DIGITAL pins can be used as INPUT and OUTPUT.",
}


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
    card.body = NEW_BODY
    card.question = NEW_QUESTION
    card.explanation = NEW_EXPLANATION
    card.action_payload = NEW_ACTION_PAYLOAD
    card.save(
        update_fields=[
            "title",
            "body",
            "question",
            "explanation",
            "action_payload",
        ]
    )


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
    card.body = OLD_BODY
    card.question = OLD_QUESTION
    card.explanation = OLD_EXPLANATION
    card.action_payload = OLD_ACTION_PAYLOAD
    card.save(
        update_fields=[
            "title",
            "body",
            "question",
            "explanation",
            "action_payload",
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0155_convert_card5_to_true_false_digital_output_quiz"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
