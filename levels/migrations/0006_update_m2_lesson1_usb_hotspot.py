from django.db import migrations


def update_usb_hotspot_card(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title="Mission 2 Lesson 1").first()
    if not lesson:
        return

    LessonCard.objects.filter(lesson=lesson, order=3).update(
        title="Find the USB Port",
        body="Click the USB port on the Arduino board to reveal it.",
        image_url="/static/lessons/mission2/arduino_board.png",
        action_label="I found the USB port",
        action_payload={
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
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0005_badge_step_badgeaward_stepcompletion"),
    ]

    operations = [
        migrations.RunPython(update_usb_hotspot_card),
    ]
