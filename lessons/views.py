from django.http import Http404, HttpResponse
from django.shortcuts import render

# -------------------------------------------------------------------
# SIMPLE IN-MEMORY DATA (later we can move to database models)
# -------------------------------------------------------------------

# ===== MISSION 1: Tools =====
MISSION1_TOOL_LESSONS = {
    "cross-head-screwdriver": {
        "slug": "cross-head-screwdriver",
        "name": "Cross-head Screwdriver",
        "title": "Cross-head Screwdriver",
        "type": "tool",
        "description": (
            "Learn what a cross-head screwdriver is, how to hold it safely, "
            "and how we use it while building Pedro."
        ),
    },
    "combination-wrench": {
        "slug": "combination-wrench",
        "name": "Combination Wrench",
        "title": "Combination Wrench",
        "type": "tool",
        "description": (
            "Understand the open-end and box-end sides and when to use each "
            "while assembling Pedro."
        ),
    },
}

# ===== MISSION 1: Fasteners =====
MISSION1_FASTENER_LESSONS = {
    "screws": {
        "slug": "screws",
        "name": "Screws",
        "title": "M3 Screws",
        "type": "fastener",
        "description": (
            "Discover how screws fasten Pedro’s body and how different lengths "
            "and threads affect strength."
        ),
    },
    "plain-washers": {
        "slug": "plain-washers",
        "name": "Plain Washers",
        "title": "Plain Washers",
        "type": "fastener",
        "description": (
            "Learn how plain washers distribute load and protect Pedro’s plexiglass parts."
        ),
    },
    "spring-washers": {
        "slug": "spring-washers",
        "name": "Spring Washers",
        "title": "Spring Washers",
        "type": "fastener",
        "description": (
            "Understand how spring washers prevent screws from loosening during movement."
        ),
    },
    "nuts": {
        "slug": "nuts",
        "name": "Nuts",
        "title": "M3 Nuts",
        "type": "fastener",
        "description": "Learn how nuts clamp the robot parts together with screws.",
    },
    "torque-nuts": {
        "slug": "torque-nuts",
        "name": "Torque / Brake Nuts",
        "title": "Torque / Brake Nuts",
        "type": "fastener",
        "description": "These nuts resist vibration—critical for Pedro’s high-movement areas.",
    },
}

# ===== MISSION 2 =====
MISSION2_LESSONS = [
    {"slug": "what-is-arduino", "title": "What is Arduino?"},
    {"slug": "arduino-ide-tour", "title": "Tour of the Arduino IDE"},
    {"slug": "upload-first-sketch", "title": "Upload Your First Sketch"},
]

# ===== MISSION 3 — 6 systems =====
MISSION3_SYSTEMS = [
    {
        "slug": "pedro-body",
        "name": "System 1: Pedro's Body",
        "lessons": [
            {"slug": "build-structure", "title": "Build the Body Structure (3D video)"},
            {"slug": "electronics", "title": "Add Electronics to the Body"},
            {"slug": "code", "title": "Write the Body System Code"},
        ],
    },
    {
        "slug": "pedro-head",
        "name": "System 2: Pedro's Head",
        "lessons": [
            {"slug": "build-head", "title": "Build the Head"},
            {"slug": "head-electronics", "title": "Wire the Head Sensors"},
            {"slug": "head-code", "title": "Program Head Movements"},
        ],
    },
    {
        "slug": "pedro-tail",
        "name": "System 3: Pedro's Tail",
        "lessons": [
            {"slug": "build-tail", "title": "Build the Tail Mechanism"},
            {"slug": "tail-electronics", "title": "Add Tail Electronics"},
            {"slug": "tail-code", "title": "Program Tail Movements"},
        ],
    },
    {
        "slug": "pedro-legs",
        "name": "System 4: Pedro's Legs",
        "lessons": [
            {
                "slug": "legs-left",
                "title": "Part 1: Pedro's Legs (Left Side)",
            },
            {
                "slug": "legs-right",
                "title": "Part 2: Pedro's Legs (Right Side)",
            },
            {
                "slug": "legs-code",
                "title": "Program Pedro's Legs",
            },
        ],
    },
    {
        "slug": "pedro-battery",
        "name": "System 5: Pedro's Battery",
        "lessons": [
            {"slug": "mount-battery", "title": "Mount the Battery Safely"},
            {"slug": "battery-wiring", "title": "Wire Power to All Systems"},
            {"slug": "power-management", "title": "Power Safety & Management"},
        ],
    },
    {
        "slug": "pedro-stand",
        "name": "System 6: Pedro's Stand",
        "lessons": [
            {"slug": "build-stand", "title": "Build Pedro's Stand"},
            {"slug": "attach-robot", "title": "Attach Pedro to the Stand"},
            {"slug": "stand-testing", "title": "Test Pedro on the Stand"},
        ],
    },
]

# ===== MISSION 4 =====
MISSION4_STEPS = [
    {"slug": "assemble-frame", "title": "Connect All Systems to the Body"},
    {"slug": "final-wiring", "title": "Final Wiring & Power Check"},
    {"slug": "combine-code", "title": "Combine All System Codes"},
    {"slug": "test-robot", "title": "Test and Debug Pedro"},
]

# -------------------------------------------------------------------
# BASIC TEST
# -------------------------------------------------------------------
def lessons_test(request):
    return HttpResponse("Hello Brainiacs – lessons app is working ✅")

# -------------------------------------------------------------------
# MISSIONS HOME
# -------------------------------------------------------------------
def missions_home(request):
    return render(request, "lessons/missions_home.html")

# -------------------------------------------------------------------
# MISSION 1
# -------------------------------------------------------------------
def mission_1(request):
    return render(
        request,
        "lessons/mission_1.html",
        {
            "step1_tools": list(MISSION1_TOOL_LESSONS.values()),
            "assembly_items": list(MISSION1_FASTENER_LESSONS.values()),
        },
    )


def _get_mission1_lesson(slug):
    lesson = MISSION1_TOOL_LESSONS.get(slug) or MISSION1_FASTENER_LESSONS.get(slug)
    if not lesson:
        raise Http404("Mission 1 lesson not found")
    return lesson


def mission_1_lesson_detail(request, slug):
    lesson = _get_mission1_lesson(slug)
    return render(request, "lessons/mission_1_lesson_detail.html", {"lesson": lesson})


def mission_1_part_1_quiz(request):
    return render(
        request,
        "lessons/mission_1_lesson_detail.html",
        {
            "lesson": {
                "title": "Mission 1 – Part 1 Quiz (Tools)",
                "type": "quiz",
                "description": "Test your understanding of all tools.",
            }
        },
    )


def mission_1_part_2_quiz(request):
    return render(
        request,
        "lessons/mission_1_lesson_detail.html",
        {
            "lesson": {
                "title": "Mission 1 – Part 2 Quiz (Fasteners)",
                "type": "quiz",
                "description": "Test your knowledge of screws, washers, and nuts.",
            }
        },
    )

# -------------------------------------------------------------------
# MISSION 2
# -------------------------------------------------------------------
def mission_2_intro(request):
    return render(
        request,
        "lessons/mission_2_intro.html",
        {"lessons": MISSION2_LESSONS},
    )


def mission_2_lesson_detail(request, slug):
    lesson = next((l for l in MISSION2_LESSONS if l["slug"] == slug), None)
    if not lesson:
        raise Http404("Lesson not found")
    return render(
        request,
        "lessons/mission_2_lesson_details.html",
        {"title": lesson["title"]},
    )

# -------------------------------------------------------------------
# MISSION 3
# -------------------------------------------------------------------
def mission_3_build_pedro(request):
    return render(
        request,
        "lessons/mission_3_build_pedro.html",
        {"systems": MISSION3_SYSTEMS},
    )


def mission_3_lesson_detail(request, system_slug, lesson_slug):
    system = next((s for s in MISSION3_SYSTEMS if s["slug"] == system_slug), None)
    if not system:
        raise Http404("System not found")

    lesson = next((l for l in system["lessons"] if l["slug"] == lesson_slug), None)
    if not lesson:
        raise Http404("Lesson not found")

    return render(
        request,
        "lessons/mission_3_lesson_detail.html",
        {"system": system, "lesson": lesson},
    )

# -------------------------------------------------------------------
# MISSION 4
# -------------------------------------------------------------------
def mission_4_assemble_pedro(request):
    return render(
        request,
        "lessons/mission_4_assemble_pedro.html",
        {"steps": MISSION4_STEPS},
    )


def mission_4_step_detail(request, slug):
    step = next((s for s in MISSION4_STEPS if s["slug"] == slug), None)
    if not step:
        raise Http404("Step not found")

    return render(
        request,
        "lessons/mission_4_step_detail.html",
        {"title": step["title"]},
    )
