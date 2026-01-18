from django.db import migrations


def update_usb_power_port_microcontroller_bounds_v3(apps, schema_editor):
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
        if hotspot.get("id") != "microcontroller":
            continue
        hotspot["bounds"] = {
            "left": 44.8,
            "top": 61.0,
            "width": 51.0,
            "height": 18.9,
        }
        updated = True
        break

    if not updated:
        return

    payload["hotspots"] = hotspots
    LessonCard.objects.filter(id=card.id).update(action_payload=payload)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0046_update_usb_power_port_microcontroller_bounds_v2"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_microcontroller_bounds_v3),
    ]
