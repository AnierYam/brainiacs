from copy import deepcopy
from django.db import migrations


def update_power_out_pins_card2_power_pins(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Out Pins").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = deepcopy(card.action_payload or {})
    payload.setdefault("type", "image-hotspot")
    payload["target"] = "power-header"
    payload["prompt"] = (
        "Hover over the main parts to see them move, then click the power frame for the power pins."
    )
    payload["success_message"] = "You found the power pins!"
    payload["fail_message"] = payload.get("fail_message") or "Not quite. Try again."

    hotspots = list(payload.get("hotspots") or [])
    for hotspot in hotspots:
        if not isinstance(hotspot, dict):
            continue
        if hotspot.get("id") == "power-header":
            hotspot["is_target"] = True
        else:
            hotspot.pop("is_target", None)
    if hotspots:
        payload["hotspots"] = hotspots

    LessonCard.objects.filter(id=card.id).update(
        title="Find the Power Pins",
        body="Hover over the main parts to see them move, then click the power frame for the power pins.",
        action_label="I found the power pins",
        action_payload=payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0096_update_power_out_pins_card1_body_v3"),
    ]

    operations = [
        migrations.RunPython(update_power_out_pins_card2_power_pins),
    ]
