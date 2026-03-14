from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
FIRST_ORDER = 4
SECOND_ORDER = 5
TEMP_ORDER = 999


def swap_card_orders(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    first_card = LessonCard.objects.filter(lesson=lesson, order=FIRST_ORDER).first()
    second_card = LessonCard.objects.filter(lesson=lesson, order=SECOND_ORDER).first()
    if not first_card or not second_card:
        return

    first_card.order = TEMP_ORDER
    first_card.save(update_fields=["order"])

    second_card.order = FIRST_ORDER
    second_card.save(update_fields=["order"])

    first_card.order = SECOND_ORDER
    first_card.save(update_fields=["order"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0123_emphasize_changing_output_phrase"),
    ]

    operations = [
        migrations.RunPython(swap_card_orders, swap_card_orders),
    ]
