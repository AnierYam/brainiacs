from django.http import Http404, HttpResponse
from django.shortcuts import render

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


def lessons_test(request):
    return HttpResponse("Hello Brainiacs – lessons app is working ✅")


def missions_home(request):
    return render(request, "lessons/missions_home.html")


def mission_1(request):
    return render(
        request,
        "lessons/mission_1.html",
        {
            "step1_tools": list(MISSION1_TOOL_LESSONS.values()),
            "assembly_items": list(MISSION1_FASTENER_LESSONS.values()),
        },
    )


def _get_mission1_lesson_or_404(slug: str):
    lesson = MISSION1_TOOL_LESSONS.get(slug) or MISSION1_FASTENER_LESSONS.get(slug)
    if not lesson:
        raise Http404("Mission 1 lesson not found")
    return lesson


def mission_1_lesson_detail(request, slug):
    lesson = _get_mission1_lesson_or_404(slug)
    return render(request, "lessons/mission_1_lesson_detail.html", {"lesson": lesson})


def mission_1_part_1_quiz(request):
    return render(
        request,
        "lessons/mission_1_lesson_detail.html",
        {
            "lesson": {
                "title": "Mission 1 – Part 1 Quiz (Tools)",
                "type": "quiz",
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
            }
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
        "slug": "reset-button",
        "title": "Reset Button",
        "part": 1,
        "focus": "47% 16%",
        "zoom": "260%",
    },
    {
        "slug": "microcontroller",
        "title": "The Microcontroller",
        "part": 1,
        "focus": "55% 52%",
        "zoom": "170%",
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
    return render(
        request,
        "lessons/mission_2_intro.html",
        {
            "lesson1_lessons": MISSION2_LESSON1,
            "lesson2_lessons": MISSION2_LESSON2,
            "lesson3_lessons": MISSION2_LESSON3,
        },
    )


def mission_2_lesson_detail(request, slug):
    all_lessons = MISSION2_LESSON1 + MISSION2_LESSON2 + MISSION2_LESSON3
    lesson = next((l for l in all_lessons if l["slug"] == slug), None)

    if not lesson:
        raise Http404("Mission 2 lesson not found")

    return render(request, "lessons/mission_2_lesson_details.html", {"lesson": lesson})


# -------------------------------------------------------------------
# Mission 3 — Building Pedro
# -------------------------------------------------------------------

MISSION3_SYSTEMS = [
    {
        "slug": "pedro-body",
        "name": "System 1: Pedro’s Body",
        "lessons": [
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
        "name": "System 4: Pedro’s Left Legs",
        "lessons": [
            {"slug": "legs-left-structure", "title": "Build Left Legs"},
            {"slug": "legs-left-electronics", "title": "Connect Left Leg Motors"},
            {"slug": "legs-left-code", "title": "Code Left Leg Movement"},
        ],
    },
    {
        "slug": "pedro-legs-right",
        "name": "System 5: Pedro’s Right Legs",
        "lessons": [
            {"slug": "legs-right-structure", "title": "Build Right Legs"},
            {"slug": "legs-right-electronics", "title": "Connect Right Leg Motors"},
            {"slug": "legs-right-code", "title": "Code Right Leg Movement"},
        ],
    },
    {
        "slug": "pedro-battery",
        "name": "System 6: Pedro’s Battery",
        "lessons": [
            {"slug": "battery-mount", "title": "Install Battery"},
            {"slug": "battery-wire", "title": "Connect Power"},
        ],
    },
    {
        "slug": "pedro-stand",
        "name": "System 7: Pedro’s Stand",
        "lessons": [
            {"slug": "stand-structure", "title": "Build the Stand"},
        ],
    },
]


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
# Mission 4 — Assemble Pedro
# -------------------------------------------------------------------

MISSION4_STEPS = [
    {"slug": "assemble-frame", "title": "Connect All Systems to the Body"},
    {"slug": "final-wiring", "title": "Final Wiring & Power Check"},
    {"slug": "combine-code", "title": "Combine All System Codes"},
    {"slug": "test-robot", "title": "Test and Debug Pedro"},
]


def mission_4_assemble_pedro(request):
    return render(
        request,
        "lessons/mission_4_assemble_pedro.html",
        {"steps": MISSION4_STEPS},
    )


def mission_4_step_detail(request, slug):
    step = next((s for s in MISSION4_STEPS if s["slug"] == slug), None)
    if not step:
        raise Http404("Mission 4 step not found")

    return render(
        request,
        "lessons/mission_4_step_detail.html",
        {"title": step["title"]},
    )
