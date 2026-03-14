from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
ANALOG_OUT_TITLE = "Quick Check ANALOG OUT Pins"
ANALOG_IN_TITLE = "Quick Check ANALOG IN Pins"
TEMP_ORDER = 999


def swap_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    analog_out_card = LessonCard.objects.filter(
        lesson=lesson,
        title=ANALOG_OUT_TITLE,
        card_type="quiz",
    ).first()
    analog_in_card = LessonCard.objects.filter(
        lesson=lesson,
        title=ANALOG_IN_TITLE,
        card_type="quiz",
    ).first()

    if not analog_out_card or not analog_in_card:
        return

    analog_out_card.order = TEMP_ORDER
    analog_out_card.save(update_fields=["order"])

    analog_in_card.order = 6
    analog_in_card.save(update_fields=["order"])

    analog_out_card.order = 7
    analog_out_card.save(update_fields=["order"])


def swap_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    analog_out_card = LessonCard.objects.filter(
        lesson=lesson,
        title=ANALOG_OUT_TITLE,
        card_type="quiz",
    ).first()
    analog_in_card = LessonCard.objects.filter(
        lesson=lesson,
        title=ANALOG_IN_TITLE,
        card_type="quiz",
    ).first()

    if not analog_out_card or not analog_in_card:
        return

    analog_in_card.order = TEMP_ORDER
    analog_in_card.save(update_fields=["order"])

    analog_out_card.order = 6
    analog_out_card.save(update_fields=["order"])

    analog_in_card.order = 7
    analog_in_card.save(update_fields=["order"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0133_add_analog_out_quick_check_card"),
    ]

    operations = [
        migrations.RunPython(swap_forward, swap_backward),
    ]
