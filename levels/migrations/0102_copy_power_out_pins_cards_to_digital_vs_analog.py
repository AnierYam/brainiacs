from django.db import migrations


def copy_cards(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    source = Lesson.objects.filter(title="Mission 2 Lesson 1 - Power Out Pins").first()
    if not source:
        return

    target = Lesson.objects.filter(title="Mission 2 Lesson 1 - Digital vs Analog").first()
    if not target:
        target = Lesson.objects.create(
            system=source.system,
            title="Mission 2 Lesson 1 - Digital vs Analog",
            video_link=source.video_link,
            image=source.image,
            order=source.order + 1,
        )

    if LessonCard.objects.filter(lesson=target).exists():
        return

    for card in LessonCard.objects.filter(lesson=source).order_by("order"):
        LessonCard.objects.create(
            lesson=target,
            order=card.order,
            card_type=card.card_type,
            title=card.title,
            body=card.body,
            image_url=card.image_url,
            youtube_id=card.youtube_id,
            question=card.question,
            choice_a=card.choice_a,
            choice_b=card.choice_b,
            choice_c=card.choice_c,
            correct_choice=card.correct_choice,
            explanation=card.explanation,
            action_label=card.action_label,
            action_payload=card.action_payload,
            starter_code=card.starter_code,
        )


def remove_cards(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")
    target = Lesson.objects.filter(title="Mission 2 Lesson 1 - Digital vs Analog").first()
    if not target:
        return
    LessonCard.objects.filter(lesson=target).delete()
    target.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0101_update_power_out_pins_match_shuffle"),
    ]

    operations = [
        migrations.RunPython(copy_cards, remove_cards),
    ]
