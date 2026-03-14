from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
CARD_ORDER = 5
BOARD_IMAGE = "/static/lessons/mission2/arduino_board.png"

OLD_TITLE = "ANALOG OUT uses DIGITAL Pins"
OLD_BODY = (
    "On Arduino Uno, pins **~3, ~5, ~6, ~9, ~10, and ~11** can act like analog output.\n\n"
    "They are still digital pins, but they switch very fast to create smooth changes."
)

NEW_PAYLOAD = {
    "quiz_type": "pin-select",
    "multi_select": True,
    "board_min_width": 760,
    "board_max_width": 820,
    "alt": "Arduino Uno board showing the top digital pin header",
    "correct_feedback": "Correct! Pins 3, 5, 6, 9, 10, and 11 can output analog-like signals.",
    "partial_feedback": "Not quite. The PWM pins are the ones marked with ~.",
    "incorrect_feedback": "Not quite. The PWM pins are the ones marked with ~.",
    "options": [
        {"key": "13", "label": "13", "left": 47.0, "is_correct": False},
        {"key": "12", "label": "12", "left": 51.0, "is_correct": False},
        {"key": "11", "label": "11", "left": 55.0, "is_correct": True},
        {"key": "10", "label": "10", "left": 59.0, "is_correct": True},
        {"key": "9", "label": "9", "left": 63.0, "is_correct": True},
        {"key": "8", "label": "8", "left": 67.0, "is_correct": False},
        {"key": "7", "label": "7", "left": 71.5, "is_correct": False},
        {"key": "6", "label": "6", "left": 75.0, "is_correct": True},
        {"key": "5", "label": "5", "left": 78.5, "is_correct": True},
        {"key": "4", "label": "4", "left": 82.0, "is_correct": False},
        {"key": "3", "label": "3", "left": 85.5, "is_correct": True},
        {"key": "2", "label": "2", "left": 89.0, "is_correct": False},
        {"key": "1", "label": "1", "left": 92.5, "is_correct": False},
        {"key": "0", "label": "0", "left": 96.0, "is_correct": False},
    ],
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

    card.card_type = "quiz"
    card.title = "Which pins can OUTPUT analog-like signal?"
    card.body = "Tap all PWM (~) pins on the Arduino Uno."
    card.image_url = BOARD_IMAGE
    card.youtube_id = ""
    card.question = ""
    card.choice_a = ""
    card.choice_b = ""
    card.choice_c = ""
    card.correct_choice = ""
    card.explanation = ""
    card.action_label = ""
    card.action_payload = NEW_PAYLOAD
    card.starter_code = ""
    card.save(
        update_fields=[
            "card_type",
            "title",
            "body",
            "image_url",
            "youtube_id",
            "question",
            "choice_a",
            "choice_b",
            "choice_c",
            "correct_choice",
            "explanation",
            "action_label",
            "action_payload",
            "starter_code",
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

    card.card_type = "intro"
    card.title = OLD_TITLE
    card.body = OLD_BODY
    card.image_url = BOARD_IMAGE
    card.youtube_id = ""
    card.question = ""
    card.choice_a = ""
    card.choice_b = ""
    card.choice_c = ""
    card.correct_choice = ""
    card.explanation = ""
    card.action_label = ""
    card.action_payload = {}
    card.starter_code = ""
    card.save(
        update_fields=[
            "card_type",
            "title",
            "body",
            "image_url",
            "youtube_id",
            "question",
            "choice_a",
            "choice_b",
            "choice_c",
            "correct_choice",
            "explanation",
            "action_label",
            "action_payload",
            "starter_code",
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0126_update_digital_pwm_pins_card_title"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
