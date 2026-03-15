from copy import deepcopy
from django.db import migrations


SOURCE_LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
TARGET_LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Pinout"
BOARD_IMAGE = "/static/lessons/mission2/arduino_board.png"
FIND_DIGITAL_PROMPT = "Hover over the main parts to see them move, then click the digital pins."
FIND_DIGITAL_SUCCESS = "You found the digital pins!"
COMMON_FAIL_MESSAGE = "Not quite. Try again."
CARD_ORDERS = [1, 2, 3, 4, 5, 6, 7]

OLD_CARD_FOUR_PAYLOAD = {
    "quiz_type": "match",
    "pairs": [
        {"id": "gnd", "feature": "GND", "function": "- (minus)"},
        {"id": "5v", "feature": "5V", "function": "+ (plus)"},
    ],
    "correct_feedback": "You connected the power correctly!",
    "incorrect_feedback": "Check the + and - signs on the breadboard.",
    "shuffle_on_wrong": True,
}

DIGITAL_PIN_OPTIONS = [
    {"key": "13", "label": "13", "left": 7.5, "is_correct": True},
    {"key": "12", "label": "12", "left": 14.8, "is_correct": True},
    {"key": "11", "label": "11", "left": 22.1, "is_correct": True},
    {"key": "10", "label": "10", "left": 29.4, "is_correct": True},
    {"key": "9", "label": "9", "left": 36.7, "is_correct": True},
    {"key": "8", "label": "8", "left": 44.0, "is_correct": True},
    {"key": "7", "label": "7", "left": 52.5, "is_correct": True},
    {"key": "6", "label": "6", "left": 58.8, "is_correct": True},
    {"key": "5", "label": "5", "left": 65.1, "is_correct": True},
    {"key": "4", "label": "4", "left": 71.4, "is_correct": True},
    {"key": "3", "label": "3", "left": 77.7, "is_correct": True},
    {"key": "2", "label": "2", "left": 84.0, "is_correct": True},
    {"key": "1", "label": "1", "left": 90.3, "is_correct": True},
    {"key": "0", "label": "0", "left": 96.6, "is_correct": True},
]


def _save_card(card, values):
    for key, value in values.items():
        setattr(card, key, value)
    card.save(update_fields=list(values.keys()))


def _build_digital_hotspot_payload(source_card, prompt):
    payload = deepcopy(source_card.action_payload or {})
    payload.setdefault("type", "image-hotspot")
    payload["target"] = "digital-pins"
    payload["prompt"] = prompt
    payload["success_message"] = FIND_DIGITAL_SUCCESS
    payload["fail_message"] = COMMON_FAIL_MESSAGE
    payload.pop("overlay_image", None)

    hotspots = list(payload.get("hotspots") or [])
    for hotspot in hotspots:
        if not isinstance(hotspot, dict):
            continue
        if hotspot.get("id") == "digital-pins":
            hotspot["is_target"] = True
        else:
            hotspot.pop("is_target", None)
    if hotspots:
        payload["hotspots"] = hotspots

    return payload


def _build_digital_pin_quiz_payload(source_card):
    payload = deepcopy(source_card.action_payload or {})
    payload["quiz_type"] = "pin-select"
    payload["multi_select"] = True
    payload["board_min_width"] = 900
    payload["board_max_width"] = 980
    payload["alt"] = "Arduino Uno board showing the top digital pin header"
    payload["correct_feedback"] = "Correct! Digital pins 0 to 13 can give digital output."
    payload["partial_feedback"] = "Not quite. All the top DIGITAL pins can be used for digital output."
    payload["incorrect_feedback"] = "Not quite. All the top DIGITAL pins can be used for digital output."
    payload["options"] = deepcopy(DIGITAL_PIN_OPTIONS)
    payload["shuffle_on_wrong"] = False
    return payload


def _get_lessons(apps):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    source_lesson = Lesson.objects.filter(title=SOURCE_LESSON_TITLE).first()
    target_lesson = Lesson.objects.filter(title=TARGET_LESSON_TITLE).first()
    return LessonCard, source_lesson, target_lesson


def update_forward(apps, schema_editor):
    LessonCard, source_lesson, target_lesson = _get_lessons(apps)
    if not source_lesson or not target_lesson:
        return

    source_action_card = LessonCard.objects.filter(lesson=source_lesson, order=4).first()
    source_pin_quiz_card = LessonCard.objects.filter(lesson=source_lesson, order=5).first()
    if not source_action_card or not source_pin_quiz_card:
        return

    card_values = {
        1: {
            "card_type": "intro",
            "title": "What is Digital Input (DIGITAL IN)",
            "body": (
                "Digital input reads only two states: HIGH or LOW.\n\n"
                "On Arduino, DIGITAL pins (0-13) are used to read ***controllers with two states*** "
                "like push buttons or tilt sensors."
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
        },
        2: {
            "card_type": "action",
            "title": "Find the DIGITAL IN Pins",
            "body": FIND_DIGITAL_PROMPT,
            "image_url": BOARD_IMAGE,
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the digital pins",
            "action_payload": _build_digital_hotspot_payload(source_action_card, FIND_DIGITAL_PROMPT),
            "starter_code": "",
        },
        3: {
            "card_type": "intro",
            "title": "What is Digital Output (DIGITAL OUT)",
            "body": (
                "Arduino can create digital output using the DIGITAL pins.\n\n"
                "Digital output sends only two states: HIGH or LOW.\n\n"
                "This lets Arduino control ***components with ON / OFF output*** such as LEDs, buzzers, or relays."
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
        },
        4: {
            "card_type": "action",
            "title": "Find the DIGITAL OUT Pins",
            "body": FIND_DIGITAL_PROMPT,
            "image_url": BOARD_IMAGE,
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the digital pins",
            "action_payload": _build_digital_hotspot_payload(source_action_card, FIND_DIGITAL_PROMPT),
            "starter_code": "",
        },
        5: {
            "card_type": "quiz",
            "title": "Which pins can give DIGITAL OUTPUT?",
            "body": "Tap all DIGITAL pins on the Arduino Uno.",
            "image_url": BOARD_IMAGE,
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "",
            "action_payload": _build_digital_pin_quiz_payload(source_pin_quiz_card),
            "starter_code": "",
        },
        6: {
            "card_type": "quiz",
            "title": "Quick Check DIGITAL IN Pins",
            "body": "Choose one answer.",
            "image_url": "",
            "youtube_id": "",
            "question": "Which statement best describes digital input?",
            "choice_a": "It reads HIGH or LOW",
            "choice_b": "It reads a range of values",
            "choice_c": "It works only on PWM (~) pins",
            "correct_choice": "A",
            "explanation": "Correct! Digital input reads HIGH or LOW.",
            "action_label": "",
            "action_payload": {"selection_error_process": True},
            "starter_code": "",
        },
        7: {
            "card_type": "quiz",
            "title": "Quick Check DIGITAL OUT Pins",
            "body": "Choose true or false.",
            "image_url": "",
            "youtube_id": "",
            "question": "The same DIGITAL pins can be used as INPUT or OUTPUT.",
            "choice_a": "True",
            "choice_b": "False",
            "choice_c": "",
            "correct_choice": "A",
            "explanation": "Correct! In code, a digital pin can be set as INPUT or OUTPUT.",
            "action_label": "",
            "action_payload": {"selection_error_process": True},
            "starter_code": "",
        },
    }

    for order in CARD_ORDERS:
        card, _ = LessonCard.objects.get_or_create(lesson=target_lesson, order=order)
        _save_card(card, card_values[order])

    LessonCard.objects.filter(lesson=target_lesson).exclude(order__in=CARD_ORDERS).delete()


def update_backward(apps, schema_editor):
    LessonCard, source_lesson, target_lesson = _get_lessons(apps)
    if not source_lesson or not target_lesson:
        return

    source_action_card = LessonCard.objects.filter(lesson=source_lesson, order=4).first()
    if not source_action_card:
        return

    old_cards = {
        1: {
            "card_type": "intro",
            "title": "What is Digital Input / Output",
            "body": (
                "Digital input/output works with two states: HIGH and LOW.\n\n"
                "These pins are used for devices like buttons, buzzers, and LEDs."
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
        },
        2: {
            "card_type": "action",
            "title": "Find the Digital Pins",
            "body": FIND_DIGITAL_PROMPT,
            "image_url": BOARD_IMAGE,
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "I found the digital pins",
            "action_payload": _build_digital_hotspot_payload(source_action_card, FIND_DIGITAL_PROMPT),
            "starter_code": "",
        },
        3: {
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
        4: {
            "card_type": "quiz",
            "title": "Connect the Power Pins",
            "body": "Connect each Arduino pin to the correct side on the breadboard.",
            "image_url": "",
            "youtube_id": "",
            "question": "",
            "choice_a": "",
            "choice_b": "",
            "choice_c": "",
            "correct_choice": "",
            "explanation": "",
            "action_label": "",
            "action_payload": deepcopy(OLD_CARD_FOUR_PAYLOAD),
            "starter_code": "",
        },
    }

    for order in [1, 2, 3, 4]:
        card, _ = LessonCard.objects.get_or_create(lesson=target_lesson, order=order)
        _save_card(card, old_cards[order])

    LessonCard.objects.filter(lesson=target_lesson, order__in=[5, 6, 7]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0136_make_card7_true_false_pwm_digital_signal"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
