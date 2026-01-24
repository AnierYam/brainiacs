from django.db import migrations


def update_usb_power_port_card2_hint(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    body = (
        "Hover over the main parts to see them move, then click the USB port.\n"
        "\n"
        "HINT: Try plugging the usb cable from your kit to the Arduino Board to figure which is the USB Port"
    )

    LessonCard.objects.filter(id=card.id).update(body=body)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0058_update_usb_power_port_card2_hint_v2"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_card2_hint),
    ]
