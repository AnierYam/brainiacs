from django.db import migrations


def remove_usb_power_port_overlay_image(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    payload.pop("overlay_image", None)

    LessonCard.objects.filter(id=card.id).update(
        image_url="/static/lessons/mission2/arduino_board.png",
        action_payload=payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0017_restore_usb_power_port_hotspots_v1"),
    ]

    operations = [
        migrations.RunPython(remove_usb_power_port_overlay_image),
    ]
