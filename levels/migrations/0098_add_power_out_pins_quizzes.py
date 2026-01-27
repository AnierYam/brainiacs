from django.db import migrations


def add_power_out_pins_quizzes(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Out Pins").first()
    if not lesson:
        return

    cards_to_shift = list(
        LessonCard.objects.filter(lesson=lesson, order__gte=2).order_by("-order")
    )
    for card in cards_to_shift:
        LessonCard.objects.filter(id=card.id).update(order=card.order + 2)

    mcq_payload = {
        "multi_select": True,
        "options": [
            {"key": "A", "label": "GND", "is_correct": True},
            {"key": "B", "label": "5V", "is_correct": True},
            {"key": "C", "label": "A0", "is_correct": False},
            {"key": "D", "label": "RX", "is_correct": False},
        ],
        "correct_feedback": "GND and 5V are power pins.",
        "incorrect_feedback": "A0 and RX are not power pins.",
    }

    LessonCard.objects.create(
        lesson=lesson,
        order=2,
        card_type="quiz",
        title="Power Pins Quiz",
        body="",
        question=(
            "Which pins give power from the Arduino to the breadboard?\n"
            "(You can choose more than one answer.)"
        ),
        choice_a="",
        choice_b="",
        choice_c="",
        correct_choice="",
        explanation="",
        action_payload=mcq_payload,
    )

    match_payload = {
        "quiz_type": "match",
        "pairs": [
            {"id": "gnd", "feature": "GND", "function": "- (minus)"},
            {"id": "5v", "feature": "5V", "function": "+ (plus)"},
        ],
        "correct_feedback": "You connected the power correctly!",
        "incorrect_feedback": "Check the + and - signs on the breadboard.",
    }

    LessonCard.objects.create(
        lesson=lesson,
        order=3,
        card_type="quiz",
        title="Connect the Power Pins",
        body="Connect each Arduino pin to the correct side on the breadboard.",
        question="",
        choice_a="",
        choice_b="",
        choice_c="",
        correct_choice="",
        explanation="",
        action_payload=match_payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0097_update_power_out_pins_card2_power_pins"),
    ]

    operations = [
        migrations.RunPython(add_power_out_pins_quizzes),
    ]
