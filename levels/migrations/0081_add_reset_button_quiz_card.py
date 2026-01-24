from django.db import migrations


def add_reset_button_quiz_card(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Reset Button").first()
    if not lesson:
        return

    payload = {
        "options": [
            {"key": "A", "label": "It turns off the power completely"},
            {"key": "B", "label": "It deletes the code from Arduino"},
            {"key": "C", "label": "It restarts the program from the beginning"},
            {"key": "D", "label": "It uploads new code"},
        ],
        "correct_feedback": (
            "Correct! ✅\n"
            "Pressing the reset button restarts the program, just like rebooting a computer."
        ),
        "incorrect_feedback": (
            "Not quite ❌\n"
            "The reset button does not turn off power or delete code. It simply restarts the program."
        ),
        "instant_feedback": True,
        "lock_on_select": True,
    }

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=3,
        defaults={
            "card_type": "quiz",
            "title": "Quick Check 🔁 The Reset Button",
            "body": "",
            "question": "What happens when you press the reset button on the Arduino?",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "C",
            "explanation": (
                "Correct! ✅\n"
                "Pressing the reset button restarts the program, just like rebooting a computer."
            ),
            "action_payload": payload,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0080_update_reset_button_card1_text_v2"),
    ]

    operations = [
        migrations.RunPython(add_reset_button_quiz_card),
    ]
