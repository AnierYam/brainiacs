from django.db import migrations


def update_usb_power_port_hotspots(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1 - USB Power Port").first()
    if not lesson:
        return

    action_payload = {
        "type": "image-hotspot",
        "target": "usb-port",
        "prompt": "Hover over the main parts to see them move, then click the USB port.",
        "alt": "Arduino Uno board",
        "bounds": {
            "left": 0.6,
            "top": 22.1,
            "width": 21.9,
            "height": 22.1,
        },
        "hotspots": [
            {
                "id": "reset-button",
                "label": "Reset button",
                "bounds": {"left": 12.3, "top": 2.9, "width": 10.4, "height": 14.7},
            },
            {
                "id": "digital-pins",
                "label": "Digital pins",
                "bounds": {"left": 31.2, "top": 1.5, "width": 64.6, "height": 7.4},
            },
            {
                "id": "l-led",
                "label": "L LED",
                "bounds": {"left": 41.7, "top": 19.9, "width": 8.3, "height": 5.9},
            },
            {
                "id": "tx-rx",
                "label": "TX/RX LEDs",
                "bounds": {"left": 41.7, "top": 29.4, "width": 8.3, "height": 10.3},
            },
            {
                "id": "on-led",
                "label": "ON LED",
                "bounds": {"left": 83.3, "top": 28.7, "width": 9.4, "height": 5.9},
            },
            {
                "id": "microcontroller",
                "label": "Microcontroller",
                "bounds": {"left": 44.8, "top": 60.3, "width": 51.0, "height": 20.6},
            },
            {
                "id": "power-header",
                "label": "Power pins",
                "bounds": {"left": 43.8, "top": 91.2, "width": 28.6, "height": 6.6},
            },
            {
                "id": "analog-in",
                "label": "Analog in",
                "bounds": {"left": 72.9, "top": 91.2, "width": 21.9, "height": 6.6},
            },
            {
                "id": "barrel-jack",
                "label": "Power jack",
                "bounds": {"left": 1.0, "top": 75.7, "width": 22.9, "height": 22.1},
            },
            {
                "id": "usb-port",
                "label": "USB port",
                "is_target": True,
                "bounds": {"left": 0.6, "top": 22.1, "width": 21.9, "height": 22.1},
            },
        ],
        "success_message": "You found the USB port!",
        "fail_message": "Not quite. Try again.",
    }

    LessonCard.objects.filter(lesson=lesson, order=2).update(
        body="Hover over the main parts to see them move, then click the USB port.",
        action_payload=action_payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0011_update_usb_power_port_card1_image"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_hotspots),
    ]
