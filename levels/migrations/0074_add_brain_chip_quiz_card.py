from django.db import migrations


def add_brain_chip_quiz_card(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - The Brain Chip").first()
    if not lesson:
        return

    payload = {
        "options": [
            {"key": "A", "label": "Because it supplies power to the board"},
            {"key": "B", "label": "Because it runs the code and controls all actions"},
            {"key": "C", "label": "Because it connects the USB cable"},
            {"key": "D", "label": "Because it stores electricity"},
        ],
        "correct_feedback": (
            "Correct! ✅\n"
            "The microcontroller is the brain of Arduino because it runs your code, "
            "listens to inputs, and controls everything the board does."
        ),
        "incorrect_feedback": (
            "Not quite ❌\n"
            "The microcontroller does not supply power or store electricity. "
            "Its job is to think and control the board."
        ),
        "instant_feedback": True,
        "lock_on_select": True,
    }

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=3,
        defaults={
            "card_type": "quiz",
            "title": "Quick Check 🧠 The Brain of Arduino",
            "body": "",
            "question": "Why is the microcontroller called the brain of the Arduino board?",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "B",
            "explanation": (
                "Correct! ✅\n"
                "The microcontroller is the brain of Arduino because it runs your code, "
                "listens to inputs, and controls everything the board does."
            ),
            "action_payload": payload,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0073_update_brain_chip_card2_microcontroller"),
    ]

    operations = [
        migrations.RunPython(add_brain_chip_quiz_card),
    ]
