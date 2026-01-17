from django.db import migrations


def update_usb_power_port_cards(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson).delete()

    cards = [
        {
            "order": 1,
            "card_type": "intro",
            "title": "what is the USB Port",
            "body": (
                "It is a port used to connect the Arduino board to your PC.\n"
                "It is used for:\n"
                "- Powering your Arduino Board\n"
                "- Uploading code sketches to the Arduino Board\n"
                "- Allowing communication with your Arduino Board"
            ),
        },
        {
            "order": 2,
            "card_type": "action",
            "title": "Find the USB Port",
            "body": "Hover over the main parts to see them move, then click the USB port.",
            "image_url": "/static/lessons/mission2/arduino_board.png",
            "action_payload": {
                "type": "image-hotspot",
                "target": "usb-port",
                "prompt": "Hover over the main parts to see them move, then click the USB port.",
                "alt": "Arduino Uno board",
                "bounds": {
                    "left": 0.6,
                    "top": 22.6,
                    "width": 20.5,
                    "height": 20.5,
                },
                "hotspots": [
                    {
                        "id": "usb-port",
                        "label": "USB port",
                        "is_target": True,
                        "bounds": {
                            "left": 0.6,
                            "top": 22.6,
                            "width": 20.5,
                            "height": 20.5,
                        },
                    },
                    {
                        "id": "power-jack",
                        "label": "Power jack",
                        "bounds": {
                            "left": 4.0,
                            "top": 48.0,
                            "width": 18.0,
                            "height": 20.0,
                        },
                    },
                    {
                        "id": "reset-button",
                        "label": "Reset button",
                        "bounds": {
                            "left": 38.0,
                            "top": 12.0,
                            "width": 12.0,
                            "height": 12.0,
                        },
                    },
                    {
                        "id": "microcontroller",
                        "label": "Microcontroller",
                        "bounds": {
                            "left": 48.0,
                            "top": 42.0,
                            "width": 24.0,
                            "height": 18.0,
                        },
                    },
                    {
                        "id": "power-pins",
                        "label": "Power pins",
                        "bounds": {
                            "left": 74.0,
                            "top": 32.0,
                            "width": 18.0,
                            "height": 28.0,
                        },
                    },
                ],
                "success_message": "You found the USB port!",
                "fail_message": "Not quite. Try again.",
            },
        },
    ]

    for card in cards:
        LessonCard.objects.create(lesson=lesson, **card)


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0009_update_m2_lesson1_card2"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_cards),
    ]
