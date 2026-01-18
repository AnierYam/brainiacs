from django.db import migrations


def update_usb_power_port_tx_rx_bounds_v7(apps, schema_editor):
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
        if hotspot.get("id") != "tx-rx":
            continue
        hotspot["bounds"] = {
            "left": 39.1,
            "top": 29.1,
            "width": 10.9,
            "height": 11.2,
        }
        updated = True
        break

    if not updated:
        return

    payload["hotspots"] = hotspots
    LessonCard.objects.filter(id=card.id).update(action_payload=payload)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0037_update_usb_power_port_tx_rx_bounds_v6"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_tx_rx_bounds_v7),
    ]
