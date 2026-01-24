from django.db import migrations


def update_reset_button_card1_text_v2(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Reset Button").first()
    if not lesson:
        return

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=1,
        defaults={
            "title": "What is the reset button",
            "body": (
                "The reset button restarts the microcontroller and makes the program start again from the beginning.\n\n"
                "The program is the code that you upload from your computer to the arduino board."
            ),
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0079_update_reset_button_card1_text"),
    ]

    operations = [
        migrations.RunPython(update_reset_button_card1_text_v2),
    ]
