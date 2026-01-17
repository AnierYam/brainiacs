from django.db import migrations


def update_usb_power_port_overlay_frames(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    payload["overlay_image"] = "/static/lessons/mission2/arduino_board_highlight_frames.png"

    LessonCard.objects.filter(id=card.id).update(
        image_url="/static/lessons/mission2/arduino_board.png",
        action_payload=payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0014_update_usb_power_port_image_highlighted"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_overlay_frames),
    ]
