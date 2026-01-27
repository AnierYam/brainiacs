from django.db import migrations


def update_power_out_pins_card1_body(apps, schema_editor):
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

    body = (
        "The Power output pins connect the Arduino board to the Breadboard.\n"
        "The breadboard is used to connect the electronics to the Arduino to control them.\n"
        "Connect the GND to - and 5V to +\n"
        "We will learn about the Breadboard and Lesson 2"
    )

    LessonCard.objects.filter(
        lesson=lesson,
        order=1,
    ).update(body=body)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0091_update_power_out_pins_card1_title"),
    ]

    operations = [
        migrations.RunPython(update_power_out_pins_card1_body),
    ]
