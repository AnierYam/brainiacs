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
        "bounds": {"left": 0.0, "top": 21.2, "width": 23.5, "height": 23.8},
        "hotspots": [
            {
                "id": "reset-button",
                "label": "Reset button",
                "bounds": {"left": 10.8, "top": 0.6, "width": 13.8, "height": 19.4},
            },
            {
                "id": "digital-pins",
                "label": "Digital pins",
                "bounds": {"left": 28.5, "top": 0.6, "width": 67.9, "height": 19.9},
            },
            {
                "id": "l-led",
                "label": "L LED",
                "bounds": {"left": 39.2, "top": 15.3, "width": 15.5, "height": 13.4},
            },
            {
                "id": "tx-rx",
                "label": "TX/RX LEDs",
                "bounds": {"left": 39.3, "top": 22.6, "width": 15.4, "height": 17.9},
            },
            {
                "id": "on-led",
                "label": "ON LED",
                "bounds": {"left": 78.5, "top": 22.6, "width": 16.4, "height": 12.8},
            },
            {
                "id": "microcontroller",
                "label": "Microcontroller",
                "bounds": {"left": 44.2, "top": 59.4, "width": 52.3, "height": 22.4},
            },
            {
                "id": "power-header",
                "label": "Power pins",
                "bounds": {"left": 43.1, "top": 81.5, "width": 29.9, "height": 17.2},
            },
            {
                "id": "analog-in",
                "label": "Analog in",
                "bounds": {"left": 72.3, "top": 81.5, "width": 23.1, "height": 17.2},
            },
            {
                "id": "barrel-jack",
                "label": "Power jack",
                "bounds": {"left": 0.4, "top": 74.9, "width": 24.2, "height": 23.8},
            },
            {
                "id": "usb-port",
                "label": "USB port",
                "is_target": True,
                "bounds": {"left": 0.0, "top": 21.2, "width": 23.5, "height": 23.8},
            },
        ],
        "success_message": "You found the USB port!",
        "fail_message": "Not quite. Try again.",
    }

    LessonCard.objects.filter(lesson=lesson, order=2).update(
        action_payload=action_payload,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0012_update_usb_power_port_hotspots"),
    ]

    operations = [
        migrations.RunPython(update_usb_power_port_hotspots),
    ]
