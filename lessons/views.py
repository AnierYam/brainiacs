import copy
import json
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST
from lessons.models import (
    Badge as LessonBadge,
    BadgeAward as LessonBadgeAward,
    Step as LessonStep,
    StepCompletion as LessonStepCompletion,
    StepReview as LessonStepReview,
)
from levels.models import Lesson as LevelLesson

DEMO_MODE = True
REVIEW_XP = 5


def _get_demo_user():
    User = get_user_model()
    username_field = User.USERNAME_FIELD
    demo_value = "demo@example.com" if "email" in username_field else "demo-user"
    lookup = {username_field: demo_value}
    defaults = {"is_active": True}
    if "username" not in lookup and any(field.name == "username" for field in User._meta.fields):
        defaults["username"] = "demo-user"
    demo_user, _ = User.objects.get_or_create(**lookup, defaults=defaults)
    return demo_user


def _get_user(request):
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        return user
    if DEMO_MODE:
        return _get_demo_user()
    return None


def _completion_qs(user):
    if user:
        return LessonStepCompletion.objects.filter(user=user)
    return LessonStepCompletion.objects.none()

def _completed_step_ids(user, parent_prefix=""):
    qs = _completion_qs(user).filter(is_complete=True)
    if parent_prefix:
        qs = qs.filter(step__parent_slug__startswith=parent_prefix)
    return set(qs.values_list("step_id", flat=True))


def _award_qs(user):
    if user:
        return LessonBadgeAward.objects.filter(user=user)
    return LessonBadgeAward.objects.none()


def _get_step(slug, parent_slug):
    return LessonStep.objects.filter(slug=slug, parent_slug=parent_slug).first()


def _mission2_prereq_met(step, user):
    if not step or not user:
        return True
    if step.parent_slug != "mission-2-arduino-board" or step.slug != "usb-input":
        return True
    intro_step = _get_step("introduction", "mission-2-arduino-board")
    if not intro_step:
        return True
    return _completion_qs(user).filter(step=intro_step, is_complete=True).exists()


def _mission_prefix(parent_slug):
    if not parent_slug:
        return ""
    parts = parent_slug.split("-")
    if len(parts) >= 2 and parts[0] == "mission":
        return "-".join(parts[:2])
    return parent_slug


def _get_xp_stats(prefix, user):
    if not prefix:
        return 0, 0, 0
    steps = list(LessonStep.objects.filter(parent_slug__startswith=prefix))
    xp_max = sum(
        step.xp_on_complete + (step.xp_on_quiz_correct if step.has_quiz else 0)
        for step in steps
    )
    xp_total = (
        _completion_qs(user)
        .filter(step__parent_slug__startswith=prefix)
        .aggregate(total=Sum("xp_earned"))["total"]
        or 0
    )
    xp_percent = int((xp_total / xp_max) * 100) if xp_max else 0
    if xp_percent > 100:
        xp_percent = 100
    return xp_total, xp_max, xp_percent


def _ensure_step_completion(step, user):
    if not step or not user:
        return False
    completion, _ = LessonStepCompletion.objects.get_or_create(
        step=step,
        user=user,
        defaults={"xp_earned": 0},
    )
    if not completion.is_complete:
        completion.is_complete = True
        completion.xp_earned += step.xp_on_complete
        completion.save(update_fields=["is_complete", "xp_earned"])
        return True
    return False


def _record_quiz_pass(step, user):
    if not step or not user or not step.has_quiz:
        return False
    completion, _ = LessonStepCompletion.objects.get_or_create(
        step=step,
        user=user,
        defaults={"xp_earned": 0},
    )
    if not completion.quiz_passed:
        completion.quiz_passed = True
        completion.xp_earned += step.xp_on_quiz_correct
        completion.save(update_fields=["quiz_passed", "xp_earned"])
        return True
    return False


def _record_step_review(step, user):
    if not step or not user:
        return 0
    completion = _completion_qs(user).filter(step=step, is_complete=True).first()
    if not completion:
        return 0
    reviewed_on = timezone.localdate()
    review, created = LessonStepReview.objects.get_or_create(
        step=step,
        user=user,
        reviewed_on=reviewed_on,
        defaults={"xp_awarded": REVIEW_XP},
    )
    if not created:
        return 0
    completion.xp_earned += REVIEW_XP
    completion.save(update_fields=["xp_earned"])
    return REVIEW_XP


def _award_badges(user):
    if not user:
        return []
    awarded_ids = set(_award_qs(user).values_list("badge_id", flat=True))
    completions = _completion_qs(user)
    new_badges = []

    for badge in LessonBadge.objects.all():
        if badge.id in awarded_ids:
            continue
        earned = False

        if badge.rule_type == "group_complete":
            steps = LessonStep.objects.filter(parent_slug=badge.rule_target)
            total_steps = steps.count()
            completed_steps = completions.filter(step__in=steps, is_complete=True).count()
            earned = total_steps > 0 and completed_steps >= total_steps
        elif badge.rule_type == "mission_complete":
            steps = LessonStep.objects.filter(parent_slug__startswith=badge.rule_target)
            total_steps = steps.count()
            completed_steps = completions.filter(step__in=steps, is_complete=True).count()
            earned = total_steps > 0 and completed_steps >= total_steps

        if earned:
            LessonBadgeAward.objects.create(badge=badge, user=user)
            new_badges.append(badge)

    return new_badges


@require_POST
def step_quiz(request):
    step_id = request.POST.get("step_id")
    chosen_answer = (request.POST.get("chosen_answer") or "").strip()
    if not step_id:
        return JsonResponse({"correct": False, "xp_awarded": 0}, status=400)
    step = LessonStep.objects.filter(id=step_id).first()
    if not step or not step.has_quiz:
        return JsonResponse({"correct": False, "xp_awarded": 0}, status=404)
    if not chosen_answer:
        return JsonResponse({"correct": False, "xp_awarded": 0})

    user = _get_user(request)
    if not _mission2_prereq_met(step, user):
        return JsonResponse({"correct": False, "xp_awarded": 0}, status=403)
    xp_awarded = 0
    if user:
        changed = _record_quiz_pass(step, user)
        if changed:
            xp_awarded = step.xp_on_quiz_correct
    return JsonResponse({"correct": True, "xp_awarded": xp_awarded})


@require_POST
def step_complete(request):
    step_id = request.POST.get("step_id")
    if not step_id:
        return JsonResponse({"success": False, "xp_awarded": 0, "xp_total": 0}, status=400)

    step = LessonStep.objects.filter(id=step_id).first()
    if not step:
        return JsonResponse({"success": False, "xp_awarded": 0, "xp_total": 0}, status=404)

    user = _get_user(request)
    if not user:
        return JsonResponse({"success": False, "xp_awarded": 0, "xp_total": 0}, status=401)

    if not _mission2_prereq_met(step, user):
        prefix = _mission_prefix(step.parent_slug)
        xp_total, xp_max, xp_percent = _get_xp_stats(prefix, user)
        return JsonResponse(
            {
                "success": False,
                "xp_awarded": 0,
                "xp_total": xp_total,
                "xp_max": xp_max,
                "xp_percent": xp_percent,
            },
            status=403,
        )

    changed = _ensure_step_completion(step, user)
    if changed:
        _award_badges(user)
    xp_awarded = step.xp_on_complete if changed else 0
    if not changed:
        xp_awarded = _record_step_review(step, user)
    prefix = _mission_prefix(step.parent_slug)
    xp_total, xp_max, xp_percent = _get_xp_stats(prefix, user)
    return JsonResponse(
        {
            "success": True,
            "xp_awarded": xp_awarded,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
        }
    )

# -------------------------------------------------------------------
# Mission 1 – Know your Toolbox
# -------------------------------------------------------------------

MISSION1_TOOL_LESSONS = {
    "cross-head-screwdriver": {
        "slug": "cross-head-screwdriver",
        "name": "Cross-head Screwdriver",
        "title": "Cross-head Screwdriver",
        "type": "tool",
        "description": "Learn what a cross-head screwdriver is and how it is used when building Pedro.",
    },
    "combination-wrench": {
        "slug": "combination-wrench",
        "name": "Combination Wrench",
        "title": "Combination Wrench",
        "type": "tool",
        "description": "Understand the open-end and box-end of the combination wrench and when each is used.",
    },
}

MISSION1_FASTENER_LESSONS = {
    "screws": {
        "slug": "screws",
        "name": "Bolts",
        "title": "Bolts (M3 Pan-Head)",
        "type": "fastener",
        "description": "Bolts are used to hold Pedro's parts together. Learn lengths and how they fit with nuts.",
    },
    "plain-washers": {
        "slug": "plain-washers",
        "name": "Plain Washers",
        "title": "Plain Washers",
        "type": "fastener",
        "description": "Plain washers distribute force and prevent damage to the acrylic parts.",
    },
    "spring-washers": {
        "slug": "spring-washers",
        "name": "Spring Washers",
        "title": "Spring Washers",
        "type": "fastener",
        "description": "Spring washers create tension to prevent loosening during movement.",
    },
    "nuts": {
        "slug": "nuts",
        "name": "Nuts",
        "title": "Nuts (M3 Hex Nut)",
        "type": "fastener",
        "description": "Hex nuts work together with bolts to tighten the structure.",
    },
    "torque-nuts": {
        "slug": "torque-nuts",
        "name": "Torque Nuts",
        "title": "Torque / Brake Nuts",
        "type": "fastener",
        "description": "Torque nuts include a nylon insert that prevents vibration loosening.",
    },
}

MISSION1_ASSEMBLY_PARTS = [
    {"slug": "pedro-body", "name": "Pedro's Body", "title": "Pedro's Body", "type": "assembly", "quantity": 1, "description": "Main body plate."},
    {"slug": "breadboard-support", "name": "Breadboard Support", "title": "Breadboard Support", "type": "assembly", "quantity": 1, "description": "Support plate for the breadboard."},
    {"slug": "body-legs-connector", "name": "Body-Legs Connector", "title": "Body-Legs Connector", "type": "assembly", "quantity": 4, "description": "Connector piece between body and legs."},
    {"slug": "pedro-head", "name": "Pedro's Head", "title": "Pedro's Head", "type": "assembly", "quantity": 2, "description": "Head panel part."},
    {"slug": "head-servo-adapter", "name": "Head-Servo Adapter", "title": "Head-Servo Adapter", "type": "assembly", "quantity": 1, "description": "Adapter for mounting the head servo."},
    {"slug": "potentiometer-support", "name": "Potentiometer Support", "title": "Potentiometer Support", "type": "assembly", "quantity": 1, "description": "Support plate for the potentiometer."},
    {"slug": "dc-motor-support", "name": "DC Motor Support", "title": "DC Motor Support", "type": "assembly", "quantity": 2, "description": "Mounting support for the DC motor."},
    {"slug": "inner-motor-leg-adapter", "name": "Inner DC Motor-Leg Adapter", "title": "Inner DC Motor-Leg Adapter", "type": "assembly", "quantity": 2, "description": "Inner adapter linking motor to leg."},
    {"slug": "outer-motor-leg-adapter", "name": "Outer DC Motor-Leg Adapter", "title": "Outer DC Motor-Leg Adapter", "type": "assembly", "quantity": 2, "description": "Outer adapter linking motor to leg."},
    {"slug": "pedro-rear-leg", "name": "Pedro's Rear Leg", "title": "Pedro's Rear Leg", "type": "assembly", "quantity": 2, "description": "Rear leg piece for Pedro."},
    {"slug": "pedro-front-leg", "name": "Pedro's Front Leg", "title": "Pedro's Front Leg", "type": "assembly", "quantity": 2, "description": "Front leg piece for Pedro."},
    {"slug": "leg-motion-connector", "name": "Leg's Motion Connector", "title": "Leg's Motion Connector", "type": "assembly", "quantity": 2, "description": "Connector to transmit motion to legs."},
    {"slug": "battery-support", "name": "Battery Support", "title": "Battery Support", "type": "assembly", "quantity": 1, "description": "Support bracket for the battery."},
    {"slug": "vertical-stand-support", "name": "Vertical Stand Support", "title": "Vertical Stand Support", "type": "assembly", "quantity": 2, "description": "Vertical support for the stand."},
    {"slug": "horizontal-stand-support", "name": "Horizontal Stand Support", "title": "Horizontal Stand Support", "type": "assembly", "quantity": 1, "description": "Horizontal support for the stand."},
]


def lessons_test(request):
    return HttpResponse("Hello Brainiacs – lessons app is working ✅")


def missions_home(request):
    return render(request, "lessons/missions_home.html")


def mission_1(request):
    user = _get_user(request)
    step_map = {
        step.slug: step
        for step in LessonStep.objects.filter(parent_slug__startswith="mission-1")
    }
    completed_ids = _completed_step_ids(user, "mission-1")
    step1_tools = [dict(tool) for tool in MISSION1_TOOL_LESSONS.values()]
    for tool in step1_tools:
        step = step_map.get(tool["slug"])
        tool["is_complete"] = bool(step and step.id in completed_ids)
        if step:
            tool["name"] = step.title
            tool["title"] = step.title

    assembly_items = [dict(item) for item in MISSION1_FASTENER_LESSONS.values()]
    for item in assembly_items:
        step = step_map.get(item["slug"])
        item["is_complete"] = bool(step and step.id in completed_ids)
        if step:
            item["name"] = step.title
            item["title"] = step.title

    part1_quiz_step = step_map.get("part-1-quiz")
    part2_quiz_step = step_map.get("part-2-quiz")
    assembly_parts_step = step_map.get("assembly-parts")
    part1_quiz_complete = bool(part1_quiz_step and part1_quiz_step.id in completed_ids)
    part2_quiz_complete = bool(part2_quiz_step and part2_quiz_step.id in completed_ids)
    assembly_parts_complete = bool(assembly_parts_step and assembly_parts_step.id in completed_ids)

    xp_total, xp_max, xp_percent = _get_xp_stats("mission-1", user)
    return render(
        request,
        "lessons/mission_1.html",
        {
            "step1_tools": step1_tools,
            "assembly_items": assembly_items,
            "assembly_parts": MISSION1_ASSEMBLY_PARTS,
            "part1_quiz_complete": part1_quiz_complete,
            "part2_quiz_complete": part2_quiz_complete,
            "assembly_parts_complete": assembly_parts_complete,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
        },
    )


def _get_mission1_lesson_or_404(slug: str):
    lesson = (
        MISSION1_TOOL_LESSONS.get(slug)
        or MISSION1_FASTENER_LESSONS.get(slug)
        or next((p for p in MISSION1_ASSEMBLY_PARTS if p["slug"] == slug), None)
    )
    if not lesson:
        raise Http404("Mission 1 lesson not found")
    return lesson


def _mission1_anchor_id(lesson):
    lesson_type = lesson.get("type", "")
    if lesson_type == "assembly":
        return "lesson-assembly-parts"
    if lesson_type == "quiz":
        slug = lesson.get("slug", "")
        return f"lesson-quiz-{slug}" if slug else "lesson-quiz"
    slug = lesson.get("slug", "")
    return f"lesson-{lesson_type}-{slug}" if slug else f"lesson-{lesson_type}"


def mission_1_lesson_detail(request, slug):
    user = _get_user(request)
    lesson = _get_mission1_lesson_or_404(slug)
    step = _get_step(slug, "mission-1")
    lesson = {**lesson, "anchor_id": _mission1_anchor_id(lesson)}
    new_badges = []
    if request.method == "POST" and step:
        action = request.POST.get("action", "complete")
        if action == "quiz":
            changed = _record_quiz_pass(step, user)
            if not changed:
                _record_step_review(step, user)
        else:
            changed = _ensure_step_completion(step, user)
            if not changed:
                _record_step_review(step, user)
        if changed:
            new_badges = _award_badges(user)
    step_completed = (
        _completion_qs(user).filter(step=step, is_complete=True).exists() if step else False
    )
    xp_total, xp_max, xp_percent = _get_xp_stats("mission-1", user)
    return render(
        request,
        "lessons/mission_1_lesson_detail.html",
        {
            "lesson": lesson,
            "step_meta": step,
            "step_completed": step_completed,
            "new_badge": new_badges[0] if new_badges else None,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
        },
    )


def mission_1_part_1_quiz(request):
    user = _get_user(request)
    lesson = {
        "title": "Mission 1 - Part 1 Quiz (Tools)",
        "type": "quiz",
        "slug": "part-1",
    }
    step = _get_step("part-1-quiz", "mission-1")
    lesson["anchor_id"] = _mission1_anchor_id(lesson)
    new_badges = []
    if request.method == "POST" and step:
        action = request.POST.get("action", "complete")
        if action == "quiz":
            changed = _record_quiz_pass(step, user)
            if not changed:
                _record_step_review(step, user)
        else:
            changed = _ensure_step_completion(step, user)
            if not changed:
                _record_step_review(step, user)
        if changed:
            new_badges = _award_badges(user)
    step_completed = (
        _completion_qs(user).filter(step=step, is_complete=True).exists() if step else False
    )
    xp_total, xp_max, xp_percent = _get_xp_stats("mission-1", user)
    return render(
        request,
        "lessons/mission_1_lesson_detail.html",
        {
            "lesson": lesson,
            "step_meta": step,
            "step_completed": step_completed,
            "new_badge": new_badges[0] if new_badges else None,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
        },
    )

def mission_1_part_2_quiz(request):
    user = _get_user(request)
    lesson = {
        "title": "Mission 1 - Part 2 Quiz (Fasteners)",
        "type": "quiz",
        "slug": "part-2",
    }
    step = _get_step("part-2-quiz", "mission-1")
    lesson["anchor_id"] = _mission1_anchor_id(lesson)
    new_badges = []
    if request.method == "POST" and step:
        action = request.POST.get("action", "complete")
        if action == "quiz":
            changed = _record_quiz_pass(step, user)
            if not changed:
                _record_step_review(step, user)
        else:
            changed = _ensure_step_completion(step, user)
            if not changed:
                _record_step_review(step, user)
        if changed:
            new_badges = _award_badges(user)
    step_completed = (
        _completion_qs(user).filter(step=step, is_complete=True).exists() if step else False
    )
    xp_total, xp_max, xp_percent = _get_xp_stats("mission-1", user)
    return render(
        request,
        "lessons/mission_1_lesson_detail.html",
        {
            "lesson": lesson,
            "step_meta": step,
            "step_completed": step_completed,
            "new_badge": new_badges[0] if new_badges else None,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
        },
    )

def mission_1_assembly_parts(request):
    user = _get_user(request)
    step = _get_step("assembly-parts", "mission-1")
    xp_total, xp_max, xp_percent = _get_xp_stats("mission-1", user)
    return render(
        request,
        "lessons/mission_1_parts.html",
        {
            "parts": MISSION1_ASSEMBLY_PARTS,
            "step_meta": step,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
        },
    )


# -------------------------------------------------------------------
# Mission 2 — Pedro's Brain
# -------------------------------------------------------------------

MISSION2_LESSON1 = [
    {
        "slug": "introduction",
        "title": "Introduction",
        "part": 1,
        "focus": "50% 50%",
        "zoom": "220%",
    },
    {
        "slug": "usb-input",
        "title": "USB Input",
        "part": 1,
        "focus": "18% 24%",
        "zoom": "300%",
        # Use dedicated USB icon instead of board crop
        "image": "lessons/mission2/usb-logo-black-and-white.png",
    },
    {
        "slug": "power-input",
        "title": "Power Input",
        "part": 1,
        "focus": "30% 48%",
        "zoom": "300%",
    },
    {
        "slug": "microcontroller",
        "title": "The Brain Chip",
        "part": 1,
        "focus": "55% 52%",
        "zoom": "170%",
    },
    {
        "slug": "reset-button",
        "title": "Reset Button",
        "part": 1,
        "focus": "47% 16%",
        "zoom": "260%",
    },
    {
        "slug": "checkpoint-quiz",
        "title": "Checkpoint Quiz",
        "part": 1,
        "focus": "50% 50%",
        "zoom": "160%",
    },
    {
        "slug": "power-output",
        "title": "Power output",
        "part": 1,
        "focus": "78% 34%",
        "zoom": "280%",
    },
    {
        "slug": "digital-vs-analog",
        "title": "Digital vs. Analog",
        "part": 1,
        "focus": "84% 22%",
        "zoom": "240%",
    },
    {
        "slug": "arduino-pinout",
        "title": "The Arduino Pinout",
        "part": 1,
        "focus": "60% 48%",
        "zoom": "160%",
    },
    {
        "slug": "arduino-board-quiz",
        "title": "Arduino Board Quiz",
        "part": 1,
        "focus": "50% 50%",
        "zoom": "160%",
    },
]

MISSION2_LESSON2 = [
    {"slug": "what-is-a-breadboard", "title": "Introduction", "part": 2},
    {"slug": "breadboard-power-rails", "title": "Power Rails", "part": 2},
    {"slug": "row-and-column-connections", "title": "Row and Column Connections", "part": 2},
    {"slug": "connect-your-breadboard", "title": "Connect Your Board", "part": 2},
    {"slug": "build-your-first-circuit", "title": "Build your First Circuit", "part": 2},
]

MISSION2_LESSON3 = [
    {"slug": "installing-the-arduino-ide", "title": "Installation", "part": 3},
    {"slug": "understand-the-arduino-ide", "title": "Understanding the IDE", "part": 3},
    {"slug": "the-serial-monitor", "title": "The Serial Monitor", "part": 3},
    {"slug": "upload-your-first-code", "title": "Upload your First Code", "part": 3},
]


def mission_2_intro(request):
    user = _get_user(request)
    step_map = {
        (step.parent_slug, step.slug): step
        for step in LessonStep.objects.filter(parent_slug__startswith="mission-2-")
    }
    completed_ids = _completed_step_ids(user, "mission-2-")
    lesson1_lessons = [dict(lesson) for lesson in MISSION2_LESSON1]
    lesson2_lessons = [dict(lesson) for lesson in MISSION2_LESSON2]
    lesson3_lessons = [dict(lesson) for lesson in MISSION2_LESSON3]

    for lesson in lesson1_lessons:
        step = step_map.get(("mission-2-arduino-board", lesson["slug"]))
        lesson["is_complete"] = False
        if step:
            lesson["title"] = step.title
            lesson["content_mode"] = step.content_mode
            lesson["has_quiz"] = step.has_quiz
            lesson["is_complete"] = step.id in completed_ids

    for lesson in lesson2_lessons:
        step = step_map.get(("mission-2-breadboard", lesson["slug"]))
        lesson["is_complete"] = False
        if step:
            lesson["title"] = step.title
            lesson["content_mode"] = step.content_mode
            lesson["has_quiz"] = step.has_quiz
            lesson["is_complete"] = step.id in completed_ids

    for lesson in lesson3_lessons:
        step = step_map.get(("mission-2-arduino-ide", lesson["slug"]))
        lesson["is_complete"] = False
        if step:
            lesson["title"] = step.title
            lesson["content_mode"] = step.content_mode
            lesson["has_quiz"] = step.has_quiz
            lesson["is_complete"] = step.id in completed_ids

    xp_total, xp_max, xp_percent = _get_xp_stats("mission-2", user)
    return render(
        request,
        "lessons/mission_2_intro.html",
        {
            "lesson1_lessons": lesson1_lessons,
            "lesson2_lessons": lesson2_lessons,
            "lesson3_lessons": lesson3_lessons,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
        },
    )


def mission_2_lesson_detail(request, slug):
    user = _get_user(request)
    all_lessons = MISSION2_LESSON1 + MISSION2_LESSON2 + MISSION2_LESSON3
    lesson = next((l for l in all_lessons if l["slug"] == slug), None)

    if not lesson:
        raise Http404("Mission 2 lesson not found")

    step = LessonStep.objects.filter(
        slug=slug, parent_slug__startswith="mission-2-"
    ).first()
    if step:
        lesson = {
            **lesson,
            "title": step.title,
            "content_mode": step.content_mode,
            "has_quiz": step.has_quiz,
        }

    cards_json = "[]"
    cards_count = 0
    next_url = reverse("lessons:mission_2_page")
    lesson_slugs = [item["slug"] for item in all_lessons]
    try:
        lesson_index = lesson_slugs.index(slug)
    except ValueError:
        lesson_index = -1
    next_slug = ""
    if lesson_index >= 0 and lesson_index + 1 < len(lesson_slugs):
        next_slug = lesson_slugs[lesson_index + 1]
        next_url = reverse(
            "lessons:mission_2_lesson_detail",
            args=[next_slug],
        )
    continue_url = reverse("lessons:mission_2_intro")
    params = {}
    if lesson_index >= 0:
        params["focus_prev"] = slug
    if next_slug:
        params["focus_next"] = next_slug
    if params:
        continue_url = f"{continue_url}?{urlencode(params)}"
    if next_slug:
        continue_url = f"{continue_url}#lesson-{next_slug}"

    card_lesson_titles = {
        "introduction": "Mission 2 Lesson 1",
        "usb-input": "Mission 2 Lesson 1 - USB Power Port",
        "power-input": "Mission 2 Lesson 1 - Power Connector",
        "microcontroller": "Mission 2 Lesson 1 - The Brain Chip",
        "reset-button": "Mission 2 Lesson 1 - Reset Button",
        "checkpoint-quiz": "Mission 2 Lesson 1 - Checkpoint Quiz",
        "power-output": "Mission 2 Lesson 1 - Power Out Pins",
        "arduino-pinout": "Mission 2 Lesson 1 - Arduino Pinout",
        "arduino-board-quiz": "Mission 2 Lesson 1 - Arduino Board Quiz",
        "upload-your-first-code": "Mission 2 Lesson 3 - Upload Your First Code",
    }
    card_lesson_title = card_lesson_titles.get(lesson.get("slug"))
    if card_lesson_title and (not step or step.content_mode == "cards"):
        db_lesson = LevelLesson.objects.filter(title=card_lesson_title).first()
        if db_lesson:
            cards_payload = []
            for card in db_lesson.cards.all():
                cards_payload.append(
                    {
                        "id": card.id,
                        "order": card.order,
                        "card_type": card.card_type,
                        "title": card.title or "",
                        "body": card.body or "",
                        "image_url": card.image_url or "",
                        "youtube_id": card.youtube_id or "",
                        "question": card.question or "",
                        "choice_a": card.choice_a or "",
                        "choice_b": card.choice_b or "",
                        "choice_c": card.choice_c or "",
                        "correct_choice": card.correct_choice or "",
                        "explanation": card.explanation or "",
                        "action_label": card.action_label or "",
                        "action_payload": card.action_payload or {},
                        "starter_code": card.starter_code or "",
                    }
                )
            cards_json = json.dumps(cards_payload)
            cards_count = len(cards_payload)

    new_badges = []
    if request.method == "POST" and step:
        action = request.POST.get("action", "complete")
        if action == "quiz":
            changed = _record_quiz_pass(step, user)
            if not changed:
                _record_step_review(step, user)
        else:
            changed = _ensure_step_completion(step, user)
            if not changed:
                _record_step_review(step, user)
        if changed:
            new_badges = _award_badges(user)
    step_completed = (
        _completion_qs(user).filter(step=step, is_complete=True).exists() if step else False
    )
    step_locked = step is not None and not _mission2_prereq_met(step, user)
    xp_total, xp_max, xp_percent = _get_xp_stats("mission-2", user)

    return render(
        request,
        "lessons/mission_2_lesson_details.html",
        {
            "lesson": lesson,
            "cards_json": cards_json,
            "cards_count": cards_count,
            "step": step,
            "step_meta": step,
            "step_completed": step_completed,
            "step_locked": step_locked,
            "new_badge": new_badges[0] if new_badges else None,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
            "next_url": next_url,
            "continue_url": continue_url,
        },
    )


# -------------------------------------------------------------------
# Mission 3 — Building Pedro
# -------------------------------------------------------------------

MISSION3_SYSTEMS = [
    {
        "slug": "pedro-body",
        "name": "System 1: Pedro’s Body",
        "lessons": [
            {"slug": "body-leg-connector-front", "title": "Front Connectors"},
            {"slug": "body-leg-connector-back", "title": "Back Connectors"},
            {"slug": "build-structure", "title": "The Body Structure"},
        ],
    },
    {
        "slug": "pedro-head",
        "name": "System 2: Pedro’s Head",
        "lessons": [
            {"slug": "build-head", "title": "The Head"},
            {"slug": "head-electronics", "title": "Connecting the Eyes"},
            {"slug": "head-code", "title": "Coding the Eyes"},
        ],
    },
    {
        "slug": "pedro-tail",
        "name": "System 3: Pedro’s Tail",
        "lessons": [
            {"slug": "tail-structure", "title": "The Tail"},
            {"slug": "tail-electronics", "title": "Connecting the Tail"},
            {"slug": "tail-code", "title": "Coding the Tail"},
        ],
    },
    {
        "slug": "pedro-legs-left",
        "name": "System 4 (Part 4.1): Pedro's Left Legs",
        "lessons": [
            {"slug": "legs-left-structure", "title": "The Left Legs"},
        ],
    },
    {
        "slug": "pedro-legs-right",
        "name": "System 4 (Part 4.2): Pedro's Right Legs",
        "lessons": [
            {"slug": "legs-right-structure", "title": "The Right Legs"},
            {"slug": "legs-right-electronics", "title": "Connecting the Motor"},
            {"slug": "legs-right-code", "title": "Coding the Motor"},
        ],
    },
    {
        "slug": "pedro-battery",
        "name": "System 5: Pedro's Stand",
        "lessons": [
            {"slug": "stand-structure", "title": "The Stand"},
        ],
    },

]

MISSION3_VIDEO_IDS = {
    "body-leg-connector-front": "rJU8Zs6ZEwE",
    "body-leg-connector-back": "3wO1e-3LHg8",
    "build-structure": "bX3bHwYuTHg",
    "build-head": "5FXCceNBkoc",
    "tail-structure": "QzCg-Jz_vGg",
    "legs-left-structure": "3t6GST3vB50",
    "legs-right-structure": "qmjlCu1lLw4",
    "stand-structure": "lQjV9jTARPo",
}


def mission_3_build_pedro(request):
    user = _get_user(request)
    systems = copy.deepcopy(MISSION3_SYSTEMS)
    step_map = {
        (step.parent_slug, step.slug): step
        for step in LessonStep.objects.filter(parent_slug__startswith="mission-3-")
    }
    completed_ids = _completed_step_ids(user, "mission-3-")
    system_parent_map = {
        "pedro-body": "mission-3-system-1",
        "pedro-head": "mission-3-system-2",
        "pedro-tail": "mission-3-system-3",
        "pedro-legs-left": "mission-3-system-4-left",
        "pedro-legs-right": "mission-3-system-4-right",
        "pedro-battery": "mission-3-system-5",
    }
    for system in systems:
        parent_slug = system_parent_map.get(system["slug"])
        for lesson in system["lessons"]:
            lesson["is_complete"] = False
            if not parent_slug:
                continue
            step = step_map.get((parent_slug, lesson["slug"]))
            if step:
                lesson["title"] = step.title
                lesson["content_mode"] = step.content_mode
                lesson["is_complete"] = step.id in completed_ids

    xp_total, xp_max, xp_percent = _get_xp_stats("mission-3", user)
    return render(
        request,
        "lessons/mission_3_build_pedro.html",
        {
            "systems": systems,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
        },
    )


def mission_3_lesson_detail(request, system_slug, lesson_slug):
    user = _get_user(request)
    system = next((s for s in MISSION3_SYSTEMS if s["slug"] == system_slug), None)
    if not system:
        raise Http404("System not found")

    lesson = next((l for l in system["lessons"] if l["slug"] == lesson_slug), None)
    if not lesson:
        raise Http404("Lesson not found")

    system_parent_map = {
        "pedro-body": "mission-3-system-1",
        "pedro-head": "mission-3-system-2",
        "pedro-tail": "mission-3-system-3",
        "pedro-legs-left": "mission-3-system-4-left",
        "pedro-legs-right": "mission-3-system-4-right",
        "pedro-battery": "mission-3-system-5",
    }
    parent_slug = system_parent_map.get(system_slug, "")
    step = _get_step(lesson_slug, parent_slug) if parent_slug else None
    if step:
        lesson = {
            **lesson,
            "title": step.title,
            "content_mode": step.content_mode,
            "has_quiz": step.has_quiz,
        }

    video_id = ""
    if step and step.youtube_id:
        video_id = step.youtube_id
    else:
        video_id = MISSION3_VIDEO_IDS.get(lesson_slug, "")

    ordered_lessons = []
    for system_item in MISSION3_SYSTEMS:
        for lesson_item in system_item.get("lessons", []):
            ordered_lessons.append(
                {
                    "system": system_item["slug"],
                    "lesson": lesson_item["slug"],
                }
            )

    current_index = next(
        (
            index
            for index, item in enumerate(ordered_lessons)
            if item["system"] == system_slug and item["lesson"] == lesson_slug
        ),
        -1,
    )
    current_item = ordered_lessons[current_index] if current_index >= 0 else None
    next_item = (
        ordered_lessons[current_index + 1]
        if current_index >= 0 and current_index + 1 < len(ordered_lessons)
        else None
    )

    continue_url = reverse("lessons:mission_3_page")
    params = {}
    if current_item:
        params["focus_prev"] = f"{current_item['system']}-{current_item['lesson']}"
    if next_item:
        params["focus_next"] = f"{next_item['system']}-{next_item['lesson']}"
    if params:
        continue_url = f"{continue_url}?{urlencode(params)}"
    if next_item:
        continue_url = f"{continue_url}#lesson-{next_item['system']}-{next_item['lesson']}"

    new_badges = []
    if request.method == "POST" and step:
        action = request.POST.get("action", "complete")
        if action == "quiz":
            changed = _record_quiz_pass(step, user)
            if not changed:
                _record_step_review(step, user)
        else:
            changed = _ensure_step_completion(step, user)
            if not changed:
                _record_step_review(step, user)
        if changed:
            new_badges = _award_badges(user)
    step_completed = (
        _completion_qs(user).filter(step=step, is_complete=True).exists() if step else False
    )
    xp_total, xp_max, xp_percent = _get_xp_stats("mission-3", user)

    return render(
        request,
        "lessons/mission_3_lesson_detail.html",
        {
            "system": system,
            "lesson": lesson,
            "step": step,
            "step_meta": step,
            "step_completed": step_completed,
            "new_badge": new_badges[0] if new_badges else None,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
            "continue_url": continue_url,
            "video_id": video_id,
        },
    )


# -------------------------------------------------------------------
# Mission 4 — Assemble Pedro
# -------------------------------------------------------------------

MISSION4_STEPS = [
    {"slug": "assemble-frame", "title": "The Assembly"},
    {"slug": "final-wiring", "title": "Making Connections"},
    {"slug": "combine-code", "title": "Combining Codes"},
]

MISSION4_VIDEO_IDS = {
    "assemble-frame": "fT0HkZOsjWs",
}


def mission_4_assemble_pedro(request):
    user = _get_user(request)
    steps = [dict(step) for step in MISSION4_STEPS]
    step_map = {
        step.slug: step
        for step in LessonStep.objects.filter(parent_slug="mission-4")
    }
    completed_ids = _completed_step_ids(user, "mission-4")
    for step_item in steps:
        step = step_map.get(step_item["slug"])
        step_item["is_complete"] = False
        if step:
            step_item["title"] = step.title
            step_item["content_mode"] = step.content_mode
            step_item["is_complete"] = step.id in completed_ids

    xp_total, xp_max, xp_percent = _get_xp_stats("mission-4", user)
    return render(
        request,
        "lessons/mission_4_assemble_pedro.html",
        {
            "steps": steps,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
        },
    )


def mission_4_step_detail(request, slug):
    user = _get_user(request)
    step = next((s for s in MISSION4_STEPS if s["slug"] == slug), None)
    if not step:
        raise Http404("Mission 4 step not found")

    step_meta = _get_step(slug, "mission-4")
    if step_meta:
        step = {
            **step,
            "title": step_meta.title,
            "content_mode": step_meta.content_mode,
        }

    video_id = ""
    if step_meta and step_meta.youtube_id:
        video_id = step_meta.youtube_id
    else:
        video_id = MISSION4_VIDEO_IDS.get(slug, "")

    step_slugs = [item["slug"] for item in MISSION4_STEPS]
    try:
        step_index = step_slugs.index(slug)
    except ValueError:
        step_index = -1
    current_slug = step_slugs[step_index] if step_index >= 0 else ""
    next_slug = step_slugs[step_index + 1] if step_index >= 0 and step_index + 1 < len(step_slugs) else ""

    continue_url = reverse("lessons:mission_4_page")
    params = {}
    if current_slug:
        params["focus_prev"] = current_slug
    if next_slug:
        params["focus_next"] = next_slug
    if params:
        continue_url = f"{continue_url}?{urlencode(params)}"
    if next_slug:
        continue_url = f"{continue_url}#lesson-{next_slug}"

    new_badges = []
    if request.method == "POST" and step_meta:
        action = request.POST.get("action", "complete")
        if action == "quiz":
            changed = _record_quiz_pass(step_meta, user)
            if not changed:
                _record_step_review(step_meta, user)
        else:
            changed = _ensure_step_completion(step_meta, user)
            if not changed:
                _record_step_review(step_meta, user)
        if changed:
            new_badges = _award_badges(user)
    step_completed = (
        _completion_qs(user).filter(step=step_meta, is_complete=True).exists()
        if step_meta
        else False
    )
    xp_total, xp_max, xp_percent = _get_xp_stats("mission-4", user)

    return render(
        request,
        "lessons/mission_4_step_detail.html",
        {
            "title": step["title"],
            "slug": step["slug"],
            "step": step_meta,
            "step_meta": step_meta,
            "step_completed": step_completed,
            "new_badge": new_badges[0] if new_badges else None,
            "xp_total": xp_total,
            "xp_max": xp_max,
            "xp_percent": xp_percent,
            "can_track_progress": bool(user),
            "continue_url": continue_url,
            "video_id": video_id,
        },
    )
