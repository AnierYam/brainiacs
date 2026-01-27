from django.db import migrations


def reorder_power_out_pins_cards(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Out Pins").first()
    if not lesson:
        return

    cards = list(LessonCard.objects.filter(lesson=lesson))
    for card in cards:
        LessonCard.objects.filter(id=card.id).update(order=card.order + 100)

    LessonCard.objects.filter(lesson=lesson, title="What are the Power Out Pins").update(order=1)
    LessonCard.objects.filter(lesson=lesson, title="Find the Power Pins").update(order=2)
    LessonCard.objects.filter(lesson=lesson, title="Power Pins Quiz").update(order=3)
    LessonCard.objects.filter(lesson=lesson, title="Connect the Power Pins").update(order=4)
    LessonCard.objects.filter(
        lesson=lesson, title="Quick Check 🔁 The Reset Button"
    ).update(order=5)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0098_add_power_out_pins_quizzes"),
    ]

    operations = [
        migrations.RunPython(reorder_power_out_pins_cards),
    ]
