from django.db import migrations


PARENT_SLUG = "mission-2-arduino-board"


FORWARD_STEPS = [
    ("introduction", "Meet the Arduino", 1),
    ("power-input", "Power Connector", 2),
    ("usb-input", "USB Power Port", 3),
    ("on-led", "Power On Light", 4),
    ("microcontroller", "The Brain Chip", 5),
    ("reset-button", "Reset Button", 6),
    ("tx-rx-lights", "TX/RX Lights", 7),
    ("l-led", "The L Light (Pin 13 LED)", 8),
    ("checkpoint-quiz", "Checkpoint Quiz", 9),
    ("digital-vs-analog", "Digital vs Analog", 10),
    ("power-output", "Analog Input / Output", 11),
    ("arduino-pinout", "Digital Input / Output", 12),
    ("arduino-board-quiz", "Checkpoint Quiz", 13),
]

REVERSE_STEPS = [
    ("introduction", "Meet the Arduino", 1),
    ("usb-input", "USB Power Port", 2),
    ("power-input", "Power Connector", 3),
    ("on-led", "Power On Light", 4),
    ("reset-button", "Reset Button", 5),
    ("microcontroller", "The Brain Chip", 6),
    ("checkpoint-quiz", "Checkpoint Quiz", 7),
    ("power-output", "Power Out Pins", 8),
    ("digital-vs-analog", "Digital vs Analog", 9),
    ("arduino-pinout", "Pin Map", 10),
    ("arduino-board-quiz", "Arduino Board Quiz", 11),
]


def _upsert_steps(apps, step_rows):
    Step = apps.get_model("lessons", "Step")
    for slug, title, order in step_rows:
        Step.objects.update_or_create(
            parent_slug=PARENT_SLUG,
            slug=slug,
            defaults={
                "title": title,
                "order": order,
                "content_mode": "cards",
                "has_quiz": True,
                "xp_on_complete": 10,
                "xp_on_quiz_correct": 15,
            },
        )


def apply_forward(apps, schema_editor):
    _upsert_steps(apps, FORWARD_STEPS)


def apply_reverse(apps, schema_editor):
    Step = apps.get_model("lessons", "Step")
    Step.objects.filter(parent_slug=PARENT_SLUG, slug__in=["tx-rx-lights", "l-led"]).delete()
    _upsert_steps(apps, REVERSE_STEPS)


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0008_add_m2_power_on_light_step"),
    ]

    operations = [
        migrations.RunPython(apply_forward, apply_reverse),
    ]
