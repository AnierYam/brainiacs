from django.db import migrations


def update_brain_chip_card1(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - The Brain Chip").first()
    if not lesson:
        return

    body = (
        "The Microcontroller is the thinking chip.\n"
        "It is the part that thinks, decides and controls all the system.\n\n"
        "The thinking chip:\n"
        "- Talks to other parts\n"
        "- Runs your code\n"
        "- Follows your instructions line by line\n"
        "- Decides when actions happen"
    )

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=1,
        defaults={
            "title": "What is the Microcontroller",
            "body": body,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0070_seed_brain_chip_cards"),
    ]

    operations = [
        migrations.RunPython(update_brain_chip_card1),
    ]
