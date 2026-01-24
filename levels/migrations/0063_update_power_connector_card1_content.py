from django.db import migrations


def update_power_connector_card1_content(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Connector").first()
    if not lesson:
        return

    body = (
        "You use the power connector when the arduino board is not plugged into a USB port for power.\n"
        "\n"
        "The Power Connector accepts voltages between 7-12V.\n"
        "\n"
        "To power up the Arduino board, you can use:\n"
        "- A 9V Battery snap (available in your robotics kit)\n"
        "- A power adapter"
    )

    LessonCard.objects.filter(lesson=lesson, order=1).update(
        body=body,
        image_url="/static/lessons/mission2/power-connector-sources.png",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0062_update_power_connector_cards"),
    ]

    operations = [
        migrations.RunPython(update_power_connector_card1_content),
    ]
