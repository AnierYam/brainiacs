from copy import deepcopy
from django.db import migrations


def update_power_connector_action_card(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Connector").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = deepcopy(card.action_payload or {})
    payload.setdefault("type", "image-hotspot")
    payload["target"] = "barrel-jack"
    payload["prompt"] = "Hover over the main parts to see them move, then click the power jack."
    payload["success_message"] = "You found the power jack!"
    payload["fail_message"] = payload.get("fail_message") or "Not quite. Try again."

    hotspots = list(payload.get("hotspots") or [])
    for hotspot in hotspots:
        if not isinstance(hotspot, dict):
            continue
        if hotspot.get("id") == "barrel-jack":
            hotspot["is_target"] = True
        elif hotspot.get("id") == "usb-port":
            hotspot.pop("is_target", None)
    if hotspots:
        payload["hotspots"] = hotspots

    LessonCard.objects.filter(id=card.id).update(
        title="Find the Power Jack",
        body="Hover over the main parts to see them move, then click the power jack.",
        action_label="I found the power jack",
        action_payload=payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0063_update_power_connector_card1_content"),
    ]

    operations = [
        migrations.RunPython(update_power_connector_action_card),
    ]
