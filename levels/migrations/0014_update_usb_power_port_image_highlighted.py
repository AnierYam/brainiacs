from django.db import migrations


def update_usb_power_port_image(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson, order=2).update(
        image_url="/static/lessons/mission2/arduino_board with highlighted main parts.png"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0013_update_usb_power_port_hotspots_v2"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_image),
    ]
