from django.db import migrations


def remove_pinout_reward_card(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    pinout_lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Arduino Pinout").first()
    if pinout_lesson:
        LessonCard.objects.filter(lesson=pinout_lesson, card_type="reward").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0068_add_arduino_board_quiz_lesson"),
    ]

    operations = [
        migrations.RunPython(remove_pinout_reward_card),
    ]
