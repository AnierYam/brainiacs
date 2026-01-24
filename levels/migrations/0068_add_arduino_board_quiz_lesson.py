from django.db import migrations


def add_arduino_board_quiz_lesson(apps, schema_editor):
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

    quiz_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1 - Arduino Board Quiz",
        defaults={"order": 9},
    )

    LessonCard.objects.update_or_create(
        lesson=quiz_lesson,
        order=1,
        defaults={
            "card_type": "quiz",
            "title": "Final Quiz",
            "body": "Pick the best answer.",
            "question": "Which part is used to power the Arduino without USB?",
            "choice_a": "Power jack",
            "choice_b": "Reset button",
            "choice_c": "Digital pin",
            "correct_choice": "A",
            "explanation": "The power jack lets you power the Arduino with an external adapter.",
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0067_move_arduino_explorer_reward_card"),
    ]

    operations = [
        migrations.RunPython(add_arduino_board_quiz_lesson),
    ]
