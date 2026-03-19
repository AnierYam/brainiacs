from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 7
OLD_TITLE = "Quick Check DIGITAL OUT Pins"
OLD_BODY = "Choose true or false."
OLD_QUESTION = "The same DIGITAL pins can be used as INPUT or OUTPUT."
OLD_EXPLANATION = "Correct! In code, a digital pin can be set as INPUT or OUTPUT."
OLD_ACTION_PAYLOAD = {
    "selection_error_process": True,
}
NEW_TITLE = "~PWM pins can be used for both Digital and Analog-like output"
NEW_BODY = "Choose true or false."
NEW_QUESTION = ""
NEW_EXPLANATION = (
    "Correct! PWM (~) pins can be used as regular digital pins and can also "
    "create analog-like output."
)
NEW_ACTION_PAYLOAD = {
    "selection_error_process": True,
    "question_display": "title",
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
    card.choice_a = "True"
    card.choice_b = "False"
    card.choice_c = ""
    card.correct_choice = "A"
    card.explanation = NEW_EXPLANATION
    card.action_payload = NEW_ACTION_PAYLOAD
    card.save(
        update_fields=[
            "title",
            "body",
            "question",
            "choice_a",
            "choice_b",
            "choice_c",
            "correct_choice",
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
    card.choice_a = "True"
    card.choice_b = "False"
    card.choice_c = ""
    card.correct_choice = "A"
    card.explanation = OLD_EXPLANATION
    card.action_payload = OLD_ACTION_PAYLOAD
    card.save(
        update_fields=[
            "title",
            "body",
            "question",
            "choice_a",
            "choice_b",
            "choice_c",
            "correct_choice",
            "explanation",
            "action_payload",
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0158_update_card6_pwm_answer_wording"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
