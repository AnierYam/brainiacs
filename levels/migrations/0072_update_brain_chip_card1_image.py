from django.db import migrations


def update_brain_chip_card1_image(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - The Brain Chip").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson, order=1).update(
        image_url="/static/lessons/mission2/arduino_board.png"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0071_update_brain_chip_card1"),
    ]

    operations = [
        migrations.RunPython(update_brain_chip_card1_image),
    ]
