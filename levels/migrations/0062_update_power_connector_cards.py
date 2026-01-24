from django.db import migrations


def update_power_connector_cards(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Plug Spot").first()
    if lesson:
        Lesson.objects.filter(id=lesson.id).update(title="Mission 2 Lesson 1 - Power Connector")

    if not lesson:
        lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Connector").first()
    if not lesson:
        return

    body = (
        "You use the power connector when the arduino board is not plugged into a USB port for power.\n"
        "\n"
        "The Power Connector accepts voltages between 7-12V."
    )

    LessonCard.objects.filter(lesson=lesson, order=1).update(
        title="What is the Power Connector",
        body=body,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0061_seed_power_plug_spot_cards"),
    ]

    operations = [
        migrations.RunPython(update_power_connector_cards),
    ]
