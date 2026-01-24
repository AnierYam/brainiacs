from django.db import migrations


def move_arduino_explorer_reward_card(apps, schema_editor):
    Level = apps.get_model("levels", "Level")
    System = apps.get_model("levels", "System")
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    level = Level.objects.filter(number=1).first()
    if not level:
        return

    system = System.objects.filter(level=level, title="Mission 2: Pedro's Brain").first()
    if not system:
        return

    intro_lesson = Lesson.objects.filter(system=system, title="Mission 2 Lesson 1").first()
    reward_defaults = {
        "card_type": "reward",
        "title": "Arduino Explorer",
        "body": "Badge unlocked: Arduino Explorer.",
        "image_url": "",
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {},
        "starter_code": "",
    }

    if intro_lesson:
        existing_reward = LessonCard.objects.filter(
            lesson=intro_lesson,
            card_type="reward",
        ).first()
        if existing_reward:
            reward_defaults.update(
                {
                    "title": existing_reward.title,
                    "body": existing_reward.body,
                    "image_url": existing_reward.image_url,
                    "youtube_id": existing_reward.youtube_id,
                    "question": existing_reward.question,
                    "choice_a": existing_reward.choice_a,
                    "choice_b": existing_reward.choice_b,
                    "choice_c": existing_reward.choice_c,
                    "correct_choice": existing_reward.correct_choice,
                    "explanation": existing_reward.explanation,
                    "action_label": existing_reward.action_label,
                    "action_payload": existing_reward.action_payload,
                    "starter_code": existing_reward.starter_code,
                }
            )
        LessonCard.objects.filter(lesson=intro_lesson, card_type="reward").delete()

    pinout_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1 - Arduino Pinout",
        defaults={"order": 8},
    )

    LessonCard.objects.update_or_create(
        lesson=pinout_lesson,
        order=1,
        defaults=reward_defaults,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0066_add_power_connector_multi_quiz"),
    ]

    operations = [
        migrations.RunPython(move_arduino_explorer_reward_card),
    ]
