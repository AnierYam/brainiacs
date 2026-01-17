from django.db import migrations


def update_m2_lesson1_cards(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson).delete()

    cards = [
        {
            "order": 1,
            "card_type": "intro",
            "title": "Meet the Arduino Board",
            "body": "It is a simple computer that interacts with electronics that you connect.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
        },
        {
            "order": 2,
            "card_type": "visual",
            "title": "The Arduino Board",
            "body": (
                "This board will be controlling the electronics.\n"
                "We will explore how to control the electronics when you unlock mission 3."
            ),
        },
        {
            "order": 3,
            "card_type": "quiz",
            "title": "Quick Check",
            "body": "Pick the best answer.",
            "question": "What is the main purpose of the Arduino board?",
            "choice_a": "To run code that controls connected electronics",
            "choice_b": "To store batteries for Pedro",
            "choice_c": "To display graphics on a screen",
            "correct_choice": "A",
            "explanation": "The Arduino runs your code to control connected electronics.",
        },
        {
            "order": 4,
            "card_type": "reward",
            "title": "Nice work!",
            "body": "Badge unlocked: Arduino Explorer.",
        },
    ]

    for card in cards:
        LessonCard.objects.create(lesson=lesson, **card)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0007_update_m2_cards"),
    ]

    operations = [
        migrations.RunPython(update_m2_lesson1_cards),
    ]
