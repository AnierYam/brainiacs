from copy import deepcopy
from django.db import migrations


LESSON_TITLE = "Mission 2 Lesson 1 - Power Out Pins"
SOURCE_ORDER = 2
TARGET_ORDER = 4

OLD_TITLE = "PWM changes brightness and speed"
OLD_BODY = (
    "PWM changes how long the pin stays ON during each tiny cycle.\n\n"
    "- More ON time: brighter LED or faster motor\n"
    "- Less ON time: dimmer LED or slower motor"
)
OLD_IMAGE_URL = "/static/lessons/mission2/arduino_board.png"

NEW_TITLE = "Find the DIGITAL Pins"
NEW_BODY = "Hover over the main parts to see them move, then click the digital pins."
NEW_ACTION_LABEL = "I found the digital pins"


def update_forward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
      return

    source_card = LessonCard.objects.filter(lesson=lesson, order=SOURCE_ORDER).first()
    target_card = LessonCard.objects.filter(lesson=lesson, order=TARGET_ORDER).first()
    if not source_card or not target_card:
      return

    payload = deepcopy(source_card.action_payload or {})
    payload.setdefault("type", "image-hotspot")
    payload["target"] = "digital-pins"
    payload["prompt"] = NEW_BODY
    payload["success_message"] = "You found the digital pins!"
    payload["fail_message"] = "Not quite. Try again."
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

    target_card.card_type = "action"
    target_card.title = NEW_TITLE
    target_card.body = NEW_BODY
    target_card.image_url = source_card.image_url or OLD_IMAGE_URL
    target_card.youtube_id = ""
    target_card.question = ""
    target_card.choice_a = ""
    target_card.choice_b = ""
    target_card.choice_c = ""
    target_card.correct_choice = ""
    target_card.explanation = ""
    target_card.action_label = NEW_ACTION_LABEL
    target_card.action_payload = payload
    target_card.starter_code = ""
    target_card.save(
        update_fields=[
            "card_type",
            "title",
            "body",
            "image_url",
            "youtube_id",
            "question",
            "choice_a",
            "choice_b",
            "choice_c",
            "correct_choice",
            "explanation",
            "action_label",
            "action_payload",
            "starter_code",
        ]
    )


def update_backward(apps, schema_editor):
    Lesson = apps.get_model("levels", "Lesson")
    LessonCard = apps.get_model("levels", "LessonCard")

    lesson = Lesson.objects.filter(title=LESSON_TITLE).first()
    if not lesson:
      return

    target_card = LessonCard.objects.filter(lesson=lesson, order=TARGET_ORDER).first()
    if not target_card:
      return

    target_card.card_type = "intro"
    target_card.title = OLD_TITLE
    target_card.body = OLD_BODY
    target_card.image_url = OLD_IMAGE_URL
    target_card.youtube_id = ""
    target_card.question = ""
    target_card.choice_a = ""
    target_card.choice_b = ""
    target_card.choice_c = ""
    target_card.correct_choice = ""
    target_card.explanation = ""
    target_card.action_label = ""
    target_card.action_payload = {}
    target_card.starter_code = ""
    target_card.save(
        update_fields=[
            "card_type",
            "title",
            "body",
            "image_url",
            "youtube_id",
            "question",
            "choice_a",
            "choice_b",
            "choice_c",
            "correct_choice",
            "explanation",
            "action_label",
            "action_payload",
            "starter_code",
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("levels", "0124_swap_analog_output_cards_4_and_5"),
    ]

    operations = [
        migrations.RunPython(update_forward, update_backward),
    ]
