from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
CARD_ORDER = 6
OLD_TITLE = "Quick Check DIGITAL IN Pins"
OLD_BODY = "Choose one answer."
OLD_QUESTION = "Which statement best describes digital input?"
OLD_CHOICE_A = "It reads HIGH or LOW"
OLD_CHOICE_B = "It reads a range of values"
OLD_CHOICE_C = "It works only on PWM (~) pins"
OLD_CORRECT_CHOICE = "A"
OLD_EXPLANATION = "Correct! Digital input reads HIGH or LOW."
OLD_ACTION_PAYLOAD = {
    "selection_error_process": True,
}
NEW_TITLE = "which statements are true for DIGITAL pins"
NEW_BODY = "Select all that apply"
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
        {"key": "C", "label": "Give Analog-like output", "is_correct": False},
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

    card.title = NEW_TITLE
    card.body = NEW_BODY
    card.question = ""
    card.choice_a = ""
    card.choice_b = ""
    card.choice_c = ""
    card.correct_choice = ""
    card.explanation = ""
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
    card.choice_a = OLD_CHOICE_A
    card.choice_b = OLD_CHOICE_B
    card.choice_c = OLD_CHOICE_C
    card.correct_choice = OLD_CORRECT_CHOICE
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
        ("levels", "0156_move_card5_question_to_title_and_add_hint"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
