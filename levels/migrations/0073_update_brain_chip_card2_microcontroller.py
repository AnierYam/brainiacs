from copy import deepcopy
from django.db import migrations


def update_brain_chip_card2_microcontroller(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - The Brain Chip").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = deepcopy(card.action_payload or {})
    payload.setdefault("type", "image-hotspot")
    payload["target"] = "microcontroller"
    payload["prompt"] = "Hover over the main parts to see them move, then click the microcontroller."
    payload["success_message"] = "You found the microcontroller!"
    payload["fail_message"] = payload.get("fail_message") or "Not quite. Try again."

    hotspots = list(payload.get("hotspots") or [])
    for hotspot in hotspots:
        if not isinstance(hotspot, dict):
            continue
        if hotspot.get("id") == "microcontroller":
            hotspot["is_target"] = True
        elif hotspot.get("id") == "barrel-jack":
            hotspot.pop("is_target", None)
    if hotspots:
        payload["hotspots"] = hotspots

    LessonCard.objects.filter(id=card.id).update(
        title="Find the Microcontroller",
        body="Hover over the main parts to see them move, then click the microcontroller.",
        action_label="I found the microcontroller",
        action_payload=payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0072_update_brain_chip_card1_image"),
    ]

    operations = [
        migrations.RunPython(update_brain_chip_card2_microcontroller),
    ]
