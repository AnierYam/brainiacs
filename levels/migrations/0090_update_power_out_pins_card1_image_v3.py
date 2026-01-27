from django.db import migrations


def update_power_out_pins_card1_image(apps, schema_editor):
    Level = apps.get_model("levels", "Level")
    System = apps.get_model("levels", "System")
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    level = Level.objects.filter(number=1).first()
    if not level:
        return

    system = System.objects.filter(level=level, title="Mission 2: Pedro's Brain").first()
    if not system:
        return

    lesson = Lesson.objects.filter(
        system=system,
        title="Mission 2 Lesson 1 - Power Out Pins",
    ).first()
    if not lesson:
        return

    LessonCard.objects.filter(
        lesson=lesson,
        order=1,
    ).update(
        title="What are the Power Out Pins",
        image_url="/static/lessons/mission2/Power Out Pins - connecting to the breadboard.png",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0089_update_power_out_pins_card1_image_v2"),
    ]

    operations = [
        migrations.RunPython(update_power_out_pins_card1_image),
    ]
