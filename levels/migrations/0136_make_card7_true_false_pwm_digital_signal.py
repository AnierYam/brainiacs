from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
CARD_ORDER = 7

OLD_VALUES = {
    "body": "Choose one answer.",
    "question": "Which pins can give analog-like output?",
    "choice_a": "Pins marked with ~ like 3, 5, 6, 9, 10, 11",
    "choice_b": "All digital pins",
    "choice_c": "Only analog input pins A0-A5",
    "correct_choice": "A",
    "explanation": "Correct! The PWM (~) pins can give analog-like output.",
}

NEW_VALUES = {
    "body": "Choose true or false.",
    "question": "PWM (~) pins can also output digital signals.",
    "choice_a": "True",
    "choice_b": "False",
    "choice_c": "",
    "correct_choice": "A",
    "explanation": "Correct! PWM (~) pins can also work as regular digital pins.",
}


def _update_card(card, values):
    card.body = values["body"]
    card.question = values["question"]
    card.choice_a = values["choice_a"]
    card.choice_b = values["choice_b"]
    card.choice_c = values["choice_c"]
    card.correct_choice = values["correct_choice"]
    card.explanation = values["explanation"]
    card.save(
        update_fields=[
            "body",
            "question",
            "choice_a",
            "choice_b",
            "choice_c",
            "correct_choice",
            "explanation",
        ]
    )


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER, card_type="quiz").first()
    if not card:
        return

    _update_card(card, NEW_VALUES)


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=CARD_ORDER, card_type="quiz").first()
    if not card:
        return

    _update_card(card, OLD_VALUES)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0135_enable_selection_error_process_for_card6"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
