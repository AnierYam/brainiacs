from copy import deepcopy
from django.db import migrations


def update_power_out_pins_match_shuffle(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Out Pins").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, title="Connect the Power Pins").first()
    if not card:
        return

    payload = deepcopy(card.action_payload or {})
    payload["shuffle_on_wrong"] = True
    LessonCard.objects.filter(id=card.id).update(action_payload=payload)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0100_remove_power_out_pins_card5"),
    ]

    operations = [
        migrations.RunPython(update_power_out_pins_match_shuffle),
    ]
