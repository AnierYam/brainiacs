from django.db import migrations


def update_checkpoint_quiz_card2_match(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Checkpoint Quiz").first()
    if not lesson:
        return

    payload = {
        "quiz_type": "match",
        "pairs": [
            {
                "id": "usb-port",
                "feature": "USB Port",
                "function": "Sends code and power to the Arduino",
            },
            {
                "id": "power-jack",
                "feature": "Power Connector",
                "function": "Powers the Arduino",
            },
            {
                "id": "microcontroller",
                "feature": "Microcontroller",
                "function": "Runs the code",
            },
            {
                "id": "reset-button",
                "feature": "Reset Button",
                "function": "Restarts the program",
            },
        ],
        "correct_feedback": "Correct! ✅ You matched every feature with its function.",
        "incorrect_feedback": "Not quite ❌ Check the matches and try again.",
    }

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=2,
        defaults={
            "card_type": "quiz",
            "title": "Checkpoint Match",
            "body": "Match each Arduino feature to its function.",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_payload": payload,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0082_add_checkpoint_quiz_lesson"),
    ]

    operations = [
        migrations.RunPython(update_checkpoint_quiz_card2_match),
    ]
