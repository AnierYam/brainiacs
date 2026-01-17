from django.db import migrations


def update_lesson1_card2(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson, order=2).update(
        card_type="visual",
        title="The Arduino Board",
        body=(
            "The board will be controlling the electronics that you connect.\n"
            "We will explore how to control the electronics when you unlock mission 3."
        ),
        image_url="/static/lessons/mission2/arduino_board.png",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0008_update_m2_lesson1_cards_v2"),
    ]

    operations = [
        migrations.RunPython(update_lesson1_card2),
    ]
