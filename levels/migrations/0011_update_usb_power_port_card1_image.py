from django.db import migrations


def update_usb_power_port_card1_image(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson, order=1).update(
        image_url="/static/lessons/mission2/Arduino board with cable.png"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0010_update_usb_power_port_cards"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_card1_image),
    ]
