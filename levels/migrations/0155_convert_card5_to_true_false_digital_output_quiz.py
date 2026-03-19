from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 5
OLD_BODY = "Tap all DIGITAL pins on the Arduino Uno."
OLD_ACTION_PAYLOAD = {
    "quiz_type": "pin-select",
    "multi_select": True,
    "board_min_width": 900,
    "board_max_width": 980,
    "alt": "Arduino Uno board showing the top digital pin header",
    "correct_feedback": "Correct! Digital pins 0 to 13 can give digital output.",
    "partial_feedback": "Not quite. All the top DIGITAL pins can be used for digital output.",
    "incorrect_feedback": "Not quite. All the top DIGITAL pins can be used for digital output.",
    "options": [
        {"key": "13", "label": "13", "left": 7.5, "is_correct": True},
        {"key": "12", "label": "12", "left": 14.8, "is_correct": True},
        {"key": "11", "label": "11", "left": 22.1, "is_correct": True},
        {"key": "10", "label": "10", "left": 29.4, "is_correct": True},
        {"key": "9", "label": "9", "left": 36.7, "is_correct": True},
        {"key": "8", "label": "8", "left": 44.0, "is_correct": True},
        {"key": "7", "label": "7", "left": 52.5, "is_correct": True},
        {"key": "6", "label": "6", "left": 58.8, "is_correct": True},
        {"key": "5", "label": "5", "left": 65.1, "is_correct": True},
        {"key": "4", "label": "4", "left": 71.4, "is_correct": True},
        {"key": "3", "label": "3", "left": 77.7, "is_correct": True},
        {"key": "2", "label": "2", "left": 84.0, "is_correct": True},
        {"key": "1", "label": "1", "left": 90.3, "is_correct": True},
        {"key": "0", "label": "0", "left": 96.6, "is_correct": True},
    ],
    "shuffle_on_wrong": False,
}
NEW_BODY = "Choose true or false."
NEW_QUESTION = "The DIGITAL pins only give out Digital output."
NEW_EXPLANATION = "Correct! DIGITAL pins can be used as INPUT or OUTPUT."
NEW_ACTION_PAYLOAD = {
    "selection_error_process": True,
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

    card.body = NEW_BODY
    card.question = NEW_QUESTION
    card.choice_a = "True"
    card.choice_b = "False"
    card.choice_c = ""
    card.correct_choice = "B"
    card.explanation = NEW_EXPLANATION
    card.action_payload = NEW_ACTION_PAYLOAD
    card.save(
        update_fields=[
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

    card.body = OLD_BODY
    card.question = ""
    card.choice_a = ""
    card.choice_b = ""
    card.choice_c = ""
    card.correct_choice = ""
    card.explanation = ""
    card.action_payload = OLD_ACTION_PAYLOAD
    card.save(
        update_fields=[
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
        ("levels", "0154_update_digital_output_intro_copy"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
