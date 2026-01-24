from copy import deepcopy
from django.db import migrations


def update_reset_button_card2_target(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Reset Button").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = deepcopy(card.action_payload or {})
    payload.setdefault("type", "image-hotspot")
    payload["target"] = "reset-button"
    payload["prompt"] = "Hover over the main parts to see them move, then click the reset button."
    payload["success_message"] = "You found the reset button!"
    payload["fail_message"] = payload.get("fail_message") or "Not quite. Try again."

    hotspots = list(payload.get("hotspots") or [])
    for hotspot in hotspots:
        if not isinstance(hotspot, dict):
            continue
        if hotspot.get("id") == "reset-button":
            hotspot["is_target"] = True
        elif hotspot.get("id") == "microcontroller":
            hotspot.pop("is_target", None)
    if hotspots:
        payload["hotspots"] = hotspots

    LessonCard.objects.filter(id=card.id).update(
        title="Find the Reset Button",
        body="Hover over the main parts to see them move, then click the reset button.",
        action_label="I found the reset button",
        action_payload=payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0077_update_reset_button_card1"),
    ]

    operations = [
        migrations.RunPython(update_reset_button_card2_target),
    ]
