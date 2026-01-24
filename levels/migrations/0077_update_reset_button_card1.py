from django.db import migrations


def update_reset_button_card1(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Reset Button").first()
    if not lesson:
        return

    body = (
        "The reset button restarts the microcontroller and makes the program start again from the beginning."
    )

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=1,
        defaults={
            "title": "What is the reset button",
            "body": body,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0076_seed_reset_button_cards_v2"),
    ]

    operations = [
        migrations.RunPython(update_reset_button_card1),
    ]
