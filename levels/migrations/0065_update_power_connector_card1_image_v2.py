from django.db import migrations


def update_power_connector_card1_image(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Connector").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson, order=1).update(
        image_url="/static/lessons/mission2/power-connector-sources-v2.png",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0064_update_power_connector_action_card"),
    ]

    operations = [
        migrations.RunPython(update_power_connector_card1_image),
    ]
