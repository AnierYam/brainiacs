from django.db import migrations


def update_brain_chip_quiz_question(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - The Brain Chip").first()
    if not lesson:
        return

    LessonCard.objects.filter(
        lesson=lesson,
        order=3,
        card_type="quiz",
    ).update(question="Why is the microcontroller called the brain of the Arduino board?")


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0083_update_checkpoint_quiz_card2_match"),
    ]

    operations = [
        migrations.RunPython(update_brain_chip_quiz_question),
    ]
