from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
QUIZ_OLD_ORDER = 3
QUIZ_NEW_ORDER = 6
QUIZ_TITLE = "Quick Check ANALOG IN Pins"
BOARD_IMAGE = "/static/lessons/mission2/arduino_board.png"

CARD_THREE = {
    "card_type": "intro",
    "title": "What is ANALOG OUT?",
    "body": (
        "Arduino can create analog-like output from some DIGITAL pins.\n\n"
        "These pins are marked with a ~ symbol and use PWM (Pulse Width Modulation)."
    ),
    "image_url": BOARD_IMAGE,
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

CARD_FOUR = {
    "card_type": "intro",
    "title": "ANALOG OUT uses DIGITAL Pins",
    "body": (
        "On Arduino Uno, pins **~3, ~5, ~6, ~9, ~10, and ~11** can act like analog output.\n\n"
        "They are still digital pins, but they switch very fast to create smooth changes."
    ),
    "image_url": BOARD_IMAGE,
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

CARD_FIVE = {
    "card_type": "intro",
    "title": "PWM changes brightness and speed",
    "body": (
        "PWM changes how long the pin stays ON during each tiny cycle.\n\n"
        "- More ON time: brighter LED or faster motor\n"
        "- Less ON time: dimmer LED or slower motor"
    ),
    "image_url": BOARD_IMAGE,
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


def _get_lesson_and_cards(apps):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")
    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    return lesson, LessonCard


def update_forward(apps, schema_editor):
    lesson, LessonCard = _get_lesson_and_cards(apps)
    if not lesson:
        return

    quiz_card = LessonCard.objects.filter(
        lesson=lesson,
        order=QUIZ_OLD_ORDER,
        card_type="quiz",
    ).first()
    if not quiz_card:
        quiz_card = LessonCard.objects.filter(
            lesson=lesson,
            title=QUIZ_TITLE,
            card_type="quiz",
        ).first()
    if quiz_card:
        quiz_card.order = QUIZ_NEW_ORDER
        quiz_card.save(update_fields=["order"])

    LessonCard.objects.update_or_create(lesson=lesson, order=3, defaults=CARD_THREE)
    LessonCard.objects.update_or_create(lesson=lesson, order=4, defaults=CARD_FOUR)
    LessonCard.objects.update_or_create(lesson=lesson, order=5, defaults=CARD_FIVE)


def update_backward(apps, schema_editor):
    lesson, LessonCard = _get_lesson_and_cards(apps)
    if not lesson:
        return

    LessonCard.objects.filter(
        lesson=lesson,
        order__in=[3, 4, 5],
        title__in=[CARD_THREE["title"], CARD_FOUR["title"], CARD_FIVE["title"]],
    ).delete()

    quiz_card = LessonCard.objects.filter(
        lesson=lesson,
        order=QUIZ_NEW_ORDER,
        card_type="quiz",
    ).first()
    if not quiz_card:
        quiz_card = LessonCard.objects.filter(
            lesson=lesson,
            title=QUIZ_TITLE,
            card_type="quiz",
        ).first()
    if quiz_card:
        quiz_card.order = QUIZ_OLD_ORDER
        quiz_card.save(update_fields=["order"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0112_update_analog_quiz_card_title"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
