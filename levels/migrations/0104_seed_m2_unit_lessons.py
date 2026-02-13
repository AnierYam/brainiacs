import copy

from django.db import migrations


BASE_LESSON_TITLE = "Mission 2 Lesson 1 - Power Connector"

ORDERED_LESSON_TITLES = [
    ("Mission 2 Lesson 1", 1),
    ("Mission 2 Lesson 1 - Power Connector", 2),
    ("Mission 2 Lesson 1 - USB Power Port", 3),
    ("Mission 2 Lesson 1 - Power On Light", 4),
    ("Mission 2 Lesson 1 - The Brain Chip", 5),
    ("Mission 2 Lesson 1 - Reset Button", 6),
    ("Mission 2 Lesson 1 - TX/RX Lights", 7),
    ("Mission 2 Lesson 1 - The L Light (Pin 13 LED)", 8),
    ("Mission 2 Lesson 1 - Checkpoint Quiz", 9),
    ("Mission 2 Lesson 1 - Digital vs Analog", 10),
    ("Mission 2 Lesson 1 - Power Out Pins", 11),
    ("Mission 2 Lesson 1 - Arduino Pinout", 12),
    ("Mission 2 Lesson 1 - Arduino Board Quiz", 13),
]


def _make_hotspot_payload(payload, target, prompt, success_message):
    hotspot_payload = copy.deepcopy(payload) if isinstance(payload, dict) else {}
    hotspot_payload["target"] = target
    hotspot_payload["prompt"] = prompt
    hotspot_payload["success_message"] = success_message
    hotspot_payload["fail_message"] = "Not quite. Try again."

    hotspots = hotspot_payload.get("hotspots")
    if isinstance(hotspots, list):
        for hotspot in hotspots:
            if not isinstance(hotspot, dict):
                continue
            if hotspot.get("id") == target:
                hotspot["is_target"] = True
            else:
                hotspot.pop("is_target", None)
    return hotspot_payload


def _upsert_card(LessonCard, lesson, order, defaults):
    LessonCard.objects.update_or_create(
        lesson=lesson,
        order=order,
        defaults=defaults,
    )


def _seed_tx_rx_lesson(LessonCard, lesson, base_payload):
    _upsert_card(
        LessonCard,
        lesson,
        1,
        {
            "card_type": "intro",
            "title": "What are TX/RX Lights",
            "body": (
                "TX and RX are tiny communication lights on the Arduino.\n\n"
                "TX blinks when data is being sent, and RX blinks when data is being received."
            ),
            "image_url": "/static/lessons/mission2/arduino_board.png",
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
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        2,
        {
            "card_type": "action",
            "title": "Find the TX/RX Lights",
            "body": "Hover over the main parts to see them move, then click the TX/RX lights.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the TX/RX lights",
            "action_payload": _make_hotspot_payload(
                base_payload,
                "tx-rx",
                "Hover over the main parts to see them move, then click the TX/RX lights.",
                "You found the TX/RX lights!",
            ),
            "starter_code": "",
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        3,
        {
            "card_type": "quiz",
            "title": "Quick Check TX/RX Lights",
            "body": "Choose one answer.",
            "image_url": "",
            "youtube_id": "",
            "question": "What do the TX/RX lights indicate?",
            "choice_a": "Data communication activity",
            "choice_b": "Battery charge level",
            "choice_c": "Motor speed",
            "correct_choice": "A",
            "explanation": "Correct. TX/RX lights blink during data transmission and reception.",
            "action_label": "",
            "action_payload": {},
            "starter_code": "",
        },
    )
    LessonCard.objects.filter(lesson=lesson).exclude(order__in=[1, 2, 3]).delete()


def _seed_l_led_lesson(LessonCard, lesson, base_payload):
    _upsert_card(
        LessonCard,
        lesson,
        1,
        {
            "card_type": "intro",
            "title": "What is the L Light (Pin 13 LED)",
            "body": (
                "The L light is the built-in LED connected to digital pin 13.\n\n"
                "It is often used in starter programs to show how outputs can turn on and off."
            ),
            "image_url": "/static/lessons/mission2/arduino_board.png",
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
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        2,
        {
            "card_type": "action",
            "title": "Find the L Light (Pin 13 LED)",
            "body": "Hover over the main parts to see them move, then click the L light.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the L light",
            "action_payload": _make_hotspot_payload(
                base_payload,
                "l-led",
                "Hover over the main parts to see them move, then click the L light.",
                "You found the L light!",
            ),
            "starter_code": "",
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        3,
        {
            "card_type": "quiz",
            "title": "Quick Check Pin 13 LED",
            "body": "Choose one answer.",
            "image_url": "",
            "youtube_id": "",
            "question": "Which pin is connected to the built-in L light?",
            "choice_a": "Pin 13",
            "choice_b": "Pin A0",
            "choice_c": "Pin VIN",
            "correct_choice": "A",
            "explanation": "Correct. The built-in LED is connected to digital pin 13.",
            "action_label": "",
            "action_payload": {},
            "starter_code": "",
        },
    )
    LessonCard.objects.filter(lesson=lesson).exclude(order__in=[1, 2, 3]).delete()


def _seed_analog_io_lesson(LessonCard, lesson, base_payload):
    _upsert_card(
        LessonCard,
        lesson,
        1,
        {
            "card_type": "intro",
            "title": "What is Analog Input / Output",
            "body": (
                "Analog input reads a range of values instead of just ON or OFF.\n\n"
                "On Arduino, analog pins (A0-A5) are used to read sensors like light and potentiometers."
            ),
            "image_url": "/static/lessons/mission2/arduino_board.png",
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
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        2,
        {
            "card_type": "action",
            "title": "Find the Analog Pins",
            "body": "Hover over the main parts to see them move, then click the analog pins.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the analog pins",
            "action_payload": _make_hotspot_payload(
                base_payload,
                "analog-in",
                "Hover over the main parts to see them move, then click the analog pins.",
                "You found the analog pins!",
            ),
            "starter_code": "",
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        3,
        {
            "card_type": "quiz",
            "title": "Quick Check Analog I/O",
            "body": "Choose one answer.",
            "image_url": "",
            "youtube_id": "",
            "question": "Which statement best describes analog input?",
            "choice_a": "It reads a range of values",
            "choice_b": "It reads only HIGH or LOW",
            "choice_c": "It can only power LEDs",
            "correct_choice": "A",
            "explanation": "Correct. Analog input reads changing values from sensors.",
            "action_label": "",
            "action_payload": {},
            "starter_code": "",
        },
    )
    LessonCard.objects.filter(lesson=lesson).exclude(order__in=[1, 2, 3]).delete()


def _seed_digital_io_lesson(LessonCard, lesson, base_payload):
    _upsert_card(
        LessonCard,
        lesson,
        1,
        {
            "card_type": "intro",
            "title": "What is Digital Input / Output",
            "body": (
                "Digital input/output works with two states: HIGH and LOW.\n\n"
                "These pins are used for devices like buttons, buzzers, and LEDs."
            ),
            "image_url": "/static/lessons/mission2/arduino_board.png",
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
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        2,
        {
            "card_type": "action",
            "title": "Find the Digital Pins",
            "body": "Hover over the main parts to see them move, then click the digital pins.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the digital pins",
            "action_payload": _make_hotspot_payload(
                base_payload,
                "digital-pins",
                "Hover over the main parts to see them move, then click the digital pins.",
                "You found the digital pins!",
            ),
            "starter_code": "",
        },
    )
    _upsert_card(
        LessonCard,
        lesson,
        3,
        {
            "card_type": "quiz",
            "title": "Quick Check Digital I/O",
            "body": "Choose one answer.",
            "image_url": "",
            "youtube_id": "",
            "question": "Digital pins usually work with which values?",
            "choice_a": "HIGH and LOW",
            "choice_b": "0 to 1023",
            "choice_c": "Negative voltages only",
            "correct_choice": "A",
            "explanation": "Correct. Digital I/O uses two states: HIGH and LOW.",
            "action_label": "",
            "action_payload": {},
            "starter_code": "",
        },
    )
    LessonCard.objects.filter(lesson=lesson).exclude(order__in=[1, 2, 3]).delete()


def _seed_unit3_checkpoint(LessonCard, lesson):
    _upsert_card(
        LessonCard,
        lesson,
        1,
        {
            "card_type": "quiz",
            "title": "Checkpoint Quiz",
            "body": "Choose one answer.",
            "image_url": "",
            "youtube_id": "",
            "question": "Which pins are best for reading analog sensor values?",
            "choice_a": "Analog pins (A0-A5)",
            "choice_b": "Reset button",
            "choice_c": "USB connector",
            "correct_choice": "A",
            "explanation": "Correct. Analog sensors are read through the analog pins.",
            "action_label": "",
            "action_payload": {},
            "starter_code": "",
        },
    )
    LessonCard.objects.filter(lesson=lesson).exclude(order=1).delete()


def seed_m2_unit_lessons(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    base_lesson = Lesson.objects.filter(title=BASE_LESSON_TITLE).first()
    if not base_lesson:
        return

    base_action_card = LessonCard.objects.filter(lesson=base_lesson, order=2).first()
    base_payload = copy.deepcopy(base_action_card.action_payload) if base_action_card else {}

    lessons_by_title = {}
    for title, order in ORDERED_LESSON_TITLES:
        lesson = Lesson.objects.filter(title=title).first()
        if not lesson:
            lesson = Lesson.objects.create(
                system=base_lesson.system,
                title=title,
                video_link=base_lesson.video_link,
                image=base_lesson.image,
                order=order,
            )
        else:
            update_fields = []
            if lesson.system_id != base_lesson.system_id:
                lesson.system_id = base_lesson.system_id
                update_fields.append("system")
            if lesson.order != order:
                lesson.order = order
                update_fields.append("order")
            if update_fields:
                lesson.save(update_fields=update_fields)
        lessons_by_title[title] = lesson

    _seed_tx_rx_lesson(LessonCard, lessons_by_title["Mission 2 Lesson 1 - TX/RX Lights"], base_payload)
    _seed_l_led_lesson(
        LessonCard,
        lessons_by_title["Mission 2 Lesson 1 - The L Light (Pin 13 LED)"],
        base_payload,
    )
    _seed_analog_io_lesson(LessonCard, lessons_by_title["Mission 2 Lesson 1 - Power Out Pins"], base_payload)
    _seed_digital_io_lesson(LessonCard, lessons_by_title["Mission 2 Lesson 1 - Arduino Pinout"], base_payload)
    _seed_unit3_checkpoint(LessonCard, lessons_by_title["Mission 2 Lesson 1 - Arduino Board Quiz"])


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0103_add_power_on_light_lesson"),
    ]

    operations = [
        migrations.RunPython(seed_m2_unit_lessons, migrations.RunPython.noop),
    ]
