from django.db import migrations


def add_power_connector_multi_quiz(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Connector").first()
    if not lesson:
        return

    action_payload = {
        "multi_select": True,
        "options": [
            {"key": "A", "label": "USB cable", "is_correct": True},
            {"key": "B", "label": "Power jack with an external adapter", "is_correct": True},
            {"key": "C", "label": "Digital pin", "is_correct": False},
            {"key": "D", "label": "Reset button", "is_correct": False},
        ],
        "correct_feedback": (
            "Correct! ✅\n"
            "Arduino can be powered using a USB cable OR through the power jack with an external adapter."
        ),
        "partial_feedback": (
            "Almost there! 👀\n"
            "Arduino can be powered in more than one way."
        ),
        "incorrect_feedback": (
            "Not quite ❌\n"
            "Digital pins and the reset button do not power Arduino."
        ),
    }

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=3,
        defaults={
            "card_type": "quiz",
            "title": "Quick Check ⚡ Powering Arduino",
            "body": "Select all that apply.",
            "question": "Which of the following can be used to power the Arduino?",
            "choice_a": "USB cable",
            "choice_b": "Power jack with an external adapter",
            "choice_c": "Digital pin",
            "correct_choice": "",
            "explanation": "",
            "action_payload": action_payload,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0065_update_power_connector_card1_image_v2"),
    ]

    operations = [
        migrations.RunPython(add_power_connector_multi_quiz),
    ]
