from django.db import migrations


def update_power_out_pins_card1_body_hint(apps, schema_editor):
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
        "Power out pins send electricity from the Arduino to the breadboard.\n\n"
        "The breadboard lets you connect electronic parts to the Arduino.\n\n"
        "GND → – (minus)\n\n"
        "5V → + (plus)\n\n"
        "You’ll learn more about the breadboard in Lesson 2.\n\n"
        "HINT:\n\n"
        "The breadboard is in Lesson 1 of your kit\n\n"
        "Tap the image below to zoom 🔍"
    )

    LessonCard.objects.filter(
        lesson=lesson,
        order=1,
    ).update(body=body)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0093_update_power_out_pins_card1_body_spacing"),
    ]

    operations = [
        migrations.RunPython(update_power_out_pins_card1_body_hint),
    ]
