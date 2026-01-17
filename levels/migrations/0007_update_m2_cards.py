from django.db import migrations


def update_m2_lesson_cards(apps, schema_editor):
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

    intro_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1",
        defaults={"order": 1},
    )
    usb_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1 - USB Power Port",
        defaults={"order": 2},
    )
    upload_lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 3 - Upload Your First Code",
        defaults={"order": 3},
    )

    def blank_defaults():
        return {
            "title": "",
            "body": "",
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

    intro_card_1 = blank_defaults()
    intro_card_1.update(
        {
            "card_type": "intro",
            "title": "Meet the Arduino Board",
            "body": "It is a simple computer that interacts with electronics that you connect.",
        }
    )
    LessonCard.objects.update_or_create(
        lesson=intro_lesson,
        order=1,
        defaults=intro_card_1,
    )

    intro_card_2 = blank_defaults()
    intro_card_2.update(
        {
            "card_type": "visual",
            "title": "The Arduino Board",
            "body": (
                "This board will be controlling the electronics. We will explore how "
                "to control the electronics when you unlock mission 3."
            ),
            "image_url": "/static/lessons/mission2/arduino_board.png",
        }
    )
    LessonCard.objects.update_or_create(
        lesson=intro_lesson,
        order=2,
        defaults=intro_card_2,
    )

    intro_card_3 = blank_defaults()
    intro_card_3.update(
        {
            "card_type": "quiz",
            "title": "Quick Check",
            "body": "Pick the best answer.",
            "question": "What is the main purpose of the Arduino board?",
            "choice_a": "To run code that controls connected electronics",
            "choice_b": "To store batteries for Pedro",
            "choice_c": "To display graphics on a screen",
            "correct_choice": "A",
            "explanation": "The Arduino runs your code to control connected electronics.",
        }
    )
    LessonCard.objects.update_or_create(
        lesson=intro_lesson,
        order=3,
        defaults=intro_card_3,
    )

    reward_card = blank_defaults()
    reward_card.update(
        {
            "card_type": "reward",
            "title": "Nice work!",
            "body": "Badge unlocked: Arduino Explorer.",
        }
    )
    LessonCard.objects.update_or_create(
        lesson=intro_lesson,
        order=6,
        defaults=reward_card,
    )

    LessonCard.objects.filter(lesson=intro_lesson, order__in=[4, 5]).delete()

    usb_action_card = blank_defaults()
    usb_action_card.update(
        {
            "card_type": "action",
            "title": "Find the USB Port",
            "body": "Click the USB port on the Arduino board to reveal it.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "action_label": "I found the USB port",
            "action_payload": {
                "type": "image-hotspot",
                "target": "usb-port",
                "prompt": "Click the USB port on the board.",
                "alt": "Arduino Uno board",
                "bounds": {
                    "left": 0.6,
                    "top": 22.6,
                    "width": 20.5,
                    "height": 20.5,
                },
                "success_message": "You found the USB port!",
                "fail_message": "Not quite. Try again.",
            },
        }
    )
    LessonCard.objects.update_or_create(
        lesson=usb_lesson,
        order=1,
        defaults=usb_action_card,
    )

    usb_quiz_card = blank_defaults()
    usb_quiz_card.update(
        {
            "card_type": "quiz",
            "title": "Quick Check",
            "body": "Pick the best answer.",
            "question": "What is the USB port used for?",
            "choice_a": "Uploading code to the Arduino",
            "choice_b": "Powering only the LEDs",
            "choice_c": "Controlling the motors directly",
            "correct_choice": "A",
            "explanation": "The USB port powers the board and lets you upload code.",
        }
    )
    LessonCard.objects.update_or_create(
        lesson=usb_lesson,
        order=2,
        defaults=usb_quiz_card,
    )

    upload_card = blank_defaults()
    upload_card.update(
        {
            "card_type": "code",
            "title": "Blink Starter Code",
            "body": "This simple sketch blinks the built-in LED.",
            "starter_code": (
                "void setup() {\\n"
                "  pinMode(LED_BUILTIN, OUTPUT);\\n"
                "}\\n\\n"
                "void loop() {\\n"
                "  digitalWrite(LED_BUILTIN, HIGH);\\n"
                "  delay(1000);\\n"
                "  digitalWrite(LED_BUILTIN, LOW);\\n"
                "  delay(1000);\\n"
                "}\\n"
            ),
        }
    )
    LessonCard.objects.update_or_create(
        lesson=upload_lesson,
        order=1,
        defaults=upload_card,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0006_update_m2_lesson1_usb_hotspot"),
    ]

    operations = [
        migrations.RunPython(update_m2_lesson_cards),
    ]
