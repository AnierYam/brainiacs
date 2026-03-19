from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Board Quiz"
CARD_ORDER = 6

OLD_ACTION_PAYLOAD = {
    "multi_select": True,
    "question_display": "none",
    "selection_error_process": True,
    "correct_feedback": (
        "Correct! DIGITAL pins can read HIGH or LOW, give HIGH or LOW, "
        "and PWM (~) pins can also give analog-like output."
    ),
    "incorrect_feedback": (
        "Hint: DIGITAL pins read HIGH or LOW, give HIGH or LOW, "
        "and PWM (~) pins can give analog-like output."
    ),
    "partial_feedback": (
        "Hint: DIGITAL pins read HIGH or LOW, give HIGH or LOW, "
        "and PWM (~) pins can give analog-like output."
    ),
    "options": [
        {"key": "A", "label": "Read HIGH or LOW only", "is_correct": True},
        {"key": "B", "label": "Read a range of values", "is_correct": False},
        {
            "key": "C",
            "label": "Give analog-like output on PWM (~) pins",
            "is_correct": True,
        },
        {"key": "D", "label": "Give HIGH or LOW only", "is_correct": True},
    ],
}

NEW_ACTION_PAYLOAD = {
    "multi_select": True,
    "question_display": "none",
    "selection_error_process": True,
    "correct_feedback": "Correct! DIGITAL pins read and give only HIGH or LOW.",
    "incorrect_feedback": "Hint: DIGITAL pins work with HIGH or LOW for both input and output.",
    "partial_feedback": "Hint: DIGITAL pins work with HIGH or LOW for both input and output.",
    "options": [
        {"key": "A", "label": "Read HIGH or LOW only", "is_correct": True},
        {"key": "B", "label": "Read a range of values", "is_correct": False},
        {"key": "C", "label": "Give analog-like output", "is_correct": False},
        {"key": "D", "label": "Give HIGH or LOW only", "is_correct": True},
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

    card.action_payload = NEW_ACTION_PAYLOAD
    card.save(update_fields=["action_payload"])


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER).first()
    if not card:
        return

    card.action_payload = OLD_ACTION_PAYLOAD
    card.save(update_fields=["action_payload"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0164_add_second_review_clue_card"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
