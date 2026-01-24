from django.db import migrations


def clear_usb_power_port_card2_prompt(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    card = LessonCard.objects.filter(lesson=lesson, order=2).first()
    if not card:
        return

    payload = dict(card.action_payload or {})
    payload["prompt"] = ""
    LessonCard.objects.filter(id=card.id).update(action_payload=payload)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0059_update_usb_power_port_card2_hint_v3"),
    ]

    operations = [
        migrations.RunPython(clear_usb_power_port_card2_prompt),
    ]
