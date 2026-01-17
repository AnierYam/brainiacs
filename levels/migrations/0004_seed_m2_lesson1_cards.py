from django.db import migrations


def seed_lesson_cards(apps, schema_editor):
    Level = apps.get_model("levels", "Level")
    System = apps.get_model("levels", "System")
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    level, _ = Level.objects.get_or_create(
        number=1,
        defaults={
            "title": "Level 1",
            "required_xp": 0,
            "badge_name": "Starter",
        },
    )
    system, _ = System.objects.get_or_create(
        level=level,
        title="Mission 2: Pedro's Brain",
        defaults={"order": 2},
    )
    lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title="Mission 2 Lesson 1",
        defaults={"order": 1},
    )

    cards = [
        {
            "order": 1,
            "card_type": "intro",
            "title": "Welcome to Pedro's Brain",
            "body": "Meet the Arduino board and learn what each part does.",
        },
        {
            "order": 2,
            "card_type": "visual",
            "title": "The Arduino Board",
            "body": "This board powers and controls Pedro.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
        },
        {
            "order": 3,
            "card_type": "action",
            "title": "Find the USB Port",
            "body": "Locate the USB port used to upload code.",
            "action_label": "I found the USB port",
            "action_payload": {"hotspot": "usb-port"},
        },
        {
            "order": 4,
            "card_type": "quiz",
            "title": "Quick Check",
            "body": "Pick the best answer.",
            "question": "What is the USB port used for?",
            "choice_a": "Uploading code to the Arduino",
            "choice_b": "Powering only the LEDs",
            "choice_c": "Controlling the motors directly",
            "correct_choice": "A",
            "explanation": "The USB port powers the board and lets you upload code.",
        },
        {
            "order": 5,
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
        },
        {
            "order": 6,
            "card_type": "reward",
            "title": "Nice work!",
            "body": "Badge unlocked: Arduino Explorer.",
        },
    ]

    for card in cards:
        LessonCard.objects.update_or_create(
            lesson=lesson,
            order=card["order"],
            defaults=card,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0003_lessoncard"),
    ]

    operations = [
        migrations.RunPython(seed_lesson_cards),
    ]
