from django.db import migrations


def update_usb_power_port_power_header_trace(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    hotspots = list(payload.get("hotspots") or [])
    updated = False

    for hotspot in hotspots:
        if not isinstance(hotspot, dict):
            continue
        if hotspot.get("id") != "power-header":
            continue
        hotspot["bounds"] = {
            "left": 57.5,
            "top": 80.29,
            "width": 13.33,
            "height": 17.06,
        }
        hotspot["polygon"] = [
            {"x": 0, "y": 0},
            {"x": 100, "y": 0},
            {"x": 100, "y": 25.86},
            {"x": 73.44, "y": 25.86},
            {"x": 73.44, "y": 100},
            {"x": 0, "y": 100},
        ]
        updated = True
        break

    if not updated:
        return

    payload["hotspots"] = hotspots
    payload["overlay_image"] = "/static/lessons/mission2/arduino_board_power_header_trace.svg"
    LessonCard.objects.filter(id=card.id).update(action_payload=payload)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0055_update_usb_power_port_power_header_bounds_v9"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_power_header_trace),
    ]
