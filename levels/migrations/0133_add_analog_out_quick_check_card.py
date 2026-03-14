from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
ANALOG_IN_QUIZ_TITLE = "Quick Check ANALOG IN Pins"
ANALOG_OUT_QUIZ = {
    "card_type": "quiz",
    "title": "Quick Check ANALOG OUT Pins",
    "body": "Choose one answer.",
    "image_url": "",
    "youtube_id": "",
    "question": "Which pins can give analog-like output?",
    "choice_a": "Pins marked with ~ like 3, 5, 6, 9, 10, 11",
    "choice_b": "All digital pins",
    "choice_c": "Only analog input pins A0-A5",
    "correct_choice": "A",
    "explanation": "Correct! The PWM (~) pins can give analog-like output.",
    "action_label": "",
    "action_payload": {
        "selection_error_process": True,
    },
    "starter_code": "",
}


def _get_models(apps):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")
    return Lesson, LessonCard


def update_forward(apps, schema_editor):
    Lesson, LessonCard = _get_models(apps)
    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    analog_in_quiz = LessonCard.objects.filter(
        lesson=lesson,
        title=ANALOG_IN_QUIZ_TITLE,
        card_type="quiz",
    ).first()
    if analog_in_quiz and analog_in_quiz.order != 7:
        analog_in_quiz.order = 7
        analog_in_quiz.save(update_fields=["order"])

    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=6,
        defaults=ANALOG_OUT_QUIZ,
    )


def update_backward(apps, schema_editor):
    Lesson, LessonCard = _get_models(apps)
    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
        return

    LessonCard.objects.filter(
        lesson=lesson,
        order=6,
        title=ANALOG_OUT_QUIZ["title"],
        card_type="quiz",
    ).delete()

    analog_in_quiz = LessonCard.objects.filter(
        lesson=lesson,
        title=ANALOG_IN_QUIZ_TITLE,
        card_type="quiz",
    ).first()
    if analog_in_quiz and analog_in_quiz.order != 6:
        analog_in_quiz.order = 6
        analog_in_quiz.save(update_fields=["order"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0132_update_pwm_pin_quiz_title_to_output_wording"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
