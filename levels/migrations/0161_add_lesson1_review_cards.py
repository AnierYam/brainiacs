from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Arduino Board Quiz"
SYSTEM_TITLE = "Mission 2: Pedro's Brain"
BOARD_IMAGE = "/static/lessons/mission2/arduino_board.png"

HOTSPOTS = [
    {
        "id": "usb-port",
        "label": "USB Port",
        "bounds": {"left": 0.6, "top": 22.1, "width": 21.9, "height": 22.1},
    },
    {
        "id": "barrel-jack",
        "label": "Power Connector",
        "bounds": {"left": 3.85, "top": 74.26, "width": 20.52, "height": 22.65},
    },
    {
        "id": "reset-button",
        "label": "Reset Button",
        "bounds": {"left": 10.41, "top": 2.61, "width": 13.53, "height": 14.99},
    },
    {
        "id": "digital-pins",
        "label": "Digital Pins",
        "bounds": {"left": 45.35, "top": 1.5, "width": 50.2, "height": 17.1},
    },
    {
        "id": "l-led",
        "label": "L LED",
        "bounds": {"left": 40.4, "top": 20.2, "width": 8.6, "height": 5.7},
    },
    {
        "id": "tx-rx",
        "label": "TX/RX Lights",
        "bounds": {"left": 39.1, "top": 29.1, "width": 9.9, "height": 10.7},
    },
    {
        "id": "microcontroller",
        "label": "Microcontroller",
        "bounds": {"left": 44.6, "top": 61.0, "width": 51.2, "height": 18.65},
    },
    {
        "id": "analog-in",
        "label": "Analog IN Pins",
        "bounds": {"left": 72.9, "top": 80.88, "width": 22.9, "height": 17.64},
    },
]

PWM_PIN_OPTIONS = [
    {"key": "13", "label": "13", "left": 8.5, "is_correct": False},
    {"key": "12", "label": "12", "left": 16.0, "is_correct": False},
    {"key": "11", "label": "11", "left": 23.5, "is_correct": True},
    {"key": "10", "label": "10", "left": 31.0, "is_correct": True},
    {"key": "9", "label": "9", "left": 38.5, "is_correct": True},
    {"key": "8", "label": "8", "left": 46.0, "is_correct": False},
    {"key": "7", "label": "7", "left": 55.0, "is_correct": False},
    {"key": "6", "label": "6", "left": 62.5, "is_correct": True},
    {"key": "5", "label": "5", "left": 70.0, "is_correct": True},
    {"key": "4", "label": "4", "left": 77.5, "is_correct": False},
    {"key": "3", "label": "3", "left": 85.0, "is_correct": True},
    {"key": "2", "label": "2", "left": 92.5, "is_correct": False},
]

OLD_CARD = {
    1: {
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
        "explanation": "Correct! Analog pins (A0-A5) are used to read analog sensor values.",
        "action_label": "",
        "action_payload": {},
        "starter_code": "",
    }
}

REVIEW_CARDS = {
    1: {
        "card_type": "quiz",
        "title": "Board Clues",
        "body": "Use each clue to find the correct part on the Arduino board.",
        "image_url": BOARD_IMAGE,
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {
            "quiz_type": "clue-hotspot",
            "alt": "Arduino Uno board",
            "hotspots": HOTSPOTS,
            "clues": [
                {"target": "barrel-jack", "text": "I power the Arduino without USB."},
                {"target": "usb-port", "text": "I can send code and power through a cable."},
                {"target": "microcontroller", "text": "I run the code."},
                {"target": "reset-button", "text": "I restart the program."},
            ],
            "progress_feedback": "Correct. Move to the next clue.",
            "success_message": "Correct! You found each board feature from its clue.",
            "fail_message": "Not quite. Stay on this clue and try again.",
            "completed_prompt": "Every clue is solved.",
        },
        "starter_code": "",
    },
    2: {
        "card_type": "quiz",
        "title": "Match Each Part",
        "body": "Match each Arduino feature to its job.",
        "image_url": "",
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {
            "quiz_type": "match",
            "pairs": [
                {
                    "id": "usb-port",
                    "feature": "USB Port",
                    "function": "Sends code and power to the Arduino",
                },
                {
                    "id": "power-jack",
                    "feature": "Power Connector",
                    "function": "Powers the Arduino without USB",
                },
                {
                    "id": "microcontroller",
                    "feature": "Microcontroller",
                    "function": "Runs the code",
                },
                {
                    "id": "reset-button",
                    "feature": "Reset Button",
                    "function": "Restarts the program",
                },
            ],
            "correct_feedback": "Correct! You matched each feature with its function.",
            "incorrect_feedback": "Not quite. Check the matches and try again.",
            "shuffle_on_wrong": True,
            "shake_on_wrong": True,
            "color_pairs_on_select": True,
        },
        "starter_code": "",
    },
    3: {
        "card_type": "quiz",
        "title": "Tap the Output Path",
        "body": "Build the path in order from your computer to the built-in light.",
        "image_url": "",
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {
            "quiz_type": "tap-sequence",
            "prompt": "Tap these in the order a signal could move to blink the L light.",
            "items": [
                {"id": "usb-port", "label": "USB Port"},
                {"id": "microcontroller", "label": "Microcontroller"},
                {"id": "digital-pins", "label": "Digital Pins"},
                {"id": "l-led", "label": "L LED"},
            ],
            "correct_order": ["usb-port", "microcontroller", "digital-pins", "l-led"],
            "progress_feedback": "Correct. Keep going.",
            "correct_feedback": "Correct! USB brings the code in, the microcontroller runs it, and the digital pins can control the L LED.",
            "incorrect_feedback": "Not quite. Think about where the code arrives first.",
        },
        "starter_code": "",
    },
    4: {
        "card_type": "quiz",
        "title": "Sort the Arduino Parts",
        "body": "Place each part into the group that best matches its main job.",
        "image_url": "",
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {
            "quiz_type": "bucket-sort",
            "prompt": "Sort each item into Power / Link, Control, or Status.",
            "buckets": [
                {"id": "power", "label": "Power / Link"},
                {"id": "control", "label": "Control"},
                {"id": "status", "label": "Status"},
            ],
            "items": [
                {"id": "usb-port", "label": "USB Port", "bucket": "power"},
                {"id": "power-jack", "label": "Power Connector", "bucket": "power"},
                {"id": "microcontroller", "label": "Microcontroller", "bucket": "control"},
                {"id": "reset-button", "label": "Reset Button", "bucket": "control"},
                {"id": "tx-rx", "label": "TX/RX Lights", "bucket": "status"},
                {"id": "l-led", "label": "L LED", "bucket": "status"},
            ],
            "correct_feedback": "Correct! You grouped each part by its job.",
            "incorrect_feedback": "Not quite. Try sorting the parts again.",
            "shuffle_on_wrong": True,
        },
        "starter_code": "",
    },
    5: {
        "card_type": "quiz",
        "title": "Mark Each Statement True or False",
        "body": "Check every statement before you move on.",
        "image_url": "",
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {
            "quiz_type": "matrix-true-false",
            "prompt": "Mark each statement as true or false.",
            "selection_error_process": True,
            "statements": [
                {"id": "usb", "text": "The USB Port can send code and power to the Arduino.", "answer": True},
                {"id": "reset", "text": "The Reset Button runs the code.", "answer": False},
                {"id": "chip", "text": "The Microcontroller runs the code.", "answer": True},
                {"id": "analog", "text": "Analog IN pins read changing values.", "answer": True},
            ],
            "correct_feedback": "Correct! Those Lesson 1 board statements are all marked properly.",
            "incorrect_feedback": "Hint: the microcontroller runs code, and Analog IN reads changing values.",
        },
        "starter_code": "",
    },
    6: {
        "card_type": "quiz",
        "title": "which statements are true for DIGITAL pins",
        "body": "Select all that apply",
        "image_url": "",
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {
            "multi_select": True,
            "question_display": "none",
            "selection_error_process": True,
            "correct_feedback": (
                "Correct! DIGITAL pins can read HIGH or LOW, give HIGH or LOW, "
                "and PWM (~) pins can also give analog-like output."
            ),
            "incorrect_feedback": (
                "Hint: DIGITAL pins read HIGH or LOW, give HIGH or LOW, "
                "and PWM (~) pins can give analog-like output."
            ),
            "partial_feedback": (
                "Hint: DIGITAL pins read HIGH or LOW, give HIGH or LOW, "
                "and PWM (~) pins can give analog-like output."
            ),
            "options": [
                {"key": "A", "label": "Read HIGH or LOW only", "is_correct": True},
                {"key": "B", "label": "Read a range of values", "is_correct": False},
                {
                    "key": "C",
                    "label": "Give analog-like output on PWM (~) pins",
                    "is_correct": True,
                },
                {"key": "D", "label": "Give HIGH or LOW only", "is_correct": True},
            ],
        },
        "starter_code": "",
    },
    7: {
        "card_type": "quiz",
        "title": "Tap all ~PWM pins",
        "body": "Select every ~PWM pin that can give analog-like output.",
        "image_url": BOARD_IMAGE,
        "youtube_id": "",
        "question": "",
        "choice_a": "",
        "choice_b": "",
        "choice_c": "",
        "correct_choice": "",
        "explanation": "",
        "action_label": "",
        "action_payload": {
            "quiz_type": "pin-select",
            "multi_select": True,
            "board_min_width": 900,
            "board_max_width": 980,
            "alt": "Arduino Uno board showing the top digital pin header",
            "correct_feedback": "Correct! Pins 3, 5, 6, 9, 10, and 11 can output analog-like signals.",
            "partial_feedback": "Not quite. The PWM pins are the ones marked with ~.",
            "incorrect_feedback": "Not quite. The PWM pins are the ones marked with ~.",
            "options": PWM_PIN_OPTIONS,
            "shuffle_on_wrong": True,
        },
        "starter_code": "",
    },
    8: {
        "card_type": "quiz",
        "title": "~PWM pins can be used for both Digital and Analog-like output",
        "body": "Choose true or false.",
        "image_url": "",
        "youtube_id": "",
        "question": "",
        "choice_a": "True",
        "choice_b": "False",
        "choice_c": "",
        "correct_choice": "A",
        "explanation": "Correct! PWM (~) pins can be used as regular digital pins and can also create analog-like output.",
        "action_label": "",
        "action_payload": {
            "selection_error_process": True,
            "question_display": "title",
            "correct_feedback": "Correct! PWM (~) pins can act like digital pins and also create analog-like output.",
            "incorrect_feedback": "Hint: PWM (~) pins are still digital pins first.",
        },
        "starter_code": "",
    },
}


def _get_review_lesson(apps):
    Level = apps.get_model("levels", "Level")
    System = apps.get_model("levels", "System")
    Lesson = apps.get_model("levels", "Lesson")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if lesson:
        return lesson

    level = Level.objects.filter(number=1).first()
    if not level:
        return None

    system = System.objects.filter(level=level, title=SYSTEM_TITLE).first()
    if not system:
        return None

    lesson, _ = Lesson.objects.get_or_create(
        system=system,
        title=LESSON_TITLE,
        defaults={"order": 9},
    )
    return lesson


def _save_card(card, values):
    for key, value in values.items():
        setattr(card, key, value)
    card.save(update_fields=list(values.keys()))


def _replace_cards(apps, schema_editor, card_map):
    LessonCard = apps.get_model("levels", "LessonCard")
    lesson = _get_review_lesson(apps)
    if not lesson:
        return

    for order, values in card_map.items():
        card, _ = LessonCard.objects.get_or_create(lesson=lesson, order=order)
        _save_card(card, values)

    LessonCard.objects.filter(lesson=lesson).exclude(order__in=card_map.keys()).delete()


def update_forward(apps, schema_editor):
    _replace_cards(apps, schema_editor, REVIEW_CARDS)


def update_backward(apps, schema_editor):
    _replace_cards(apps, schema_editor, OLD_CARD)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0160_append_pwm_suffix_to_card4_title"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
