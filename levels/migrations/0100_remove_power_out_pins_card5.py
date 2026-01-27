from django.db import migrations


def remove_power_out_pins_card5(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Out Pins").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson, order=5).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0099_reorder_power_out_pins_cards"),
    ]

    operations = [
        migrations.RunPython(remove_power_out_pins_card5),
    ]
