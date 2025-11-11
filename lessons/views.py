from django.shortcuts import render
from django.http import HttpResponse


def test_page(request):
    """
    Simple check page: http://127.0.0.1:8000/lessons/test/
    """
    return HttpResponse("Hello Brainiacs – lessons app is working ✅")


def know_your_tools(request):
    """
    Main Level 1 lesson page:
    http://127.0.0.1:8000/lessons/know-your-tools/
    """

    # STEP 1 – basic tools
    step1_tools = [
        {
            "id": "crosshead-screwdriver",
            "name": "Cross-head Screwdriver",
            "short_description": "Used to tighten and loosen cross-head screws.",
        },
        {
            "id": "combination-wrench",
            "name": "Combination Wrench",
            "short_description": "Tightens and loosens nuts and bolts with a firm grip.",
        },
    ]

    # PART 2 – assembly accessories
    assembly_items = [
        {
            "id": "screws",
            "name": "Screws",
            "short_description": "Hold robot parts together by threading into holes.",
        },
        {
            "id": "plain-washers",
            "name": "Plain Washers",
            "short_description": "Increase contact surface and protect parts from damage.",
        },
        {
            "id": "spring-washers",
            "name": "Spring Washers",
            "short_description": "Add tension to help prevent nuts from loosening.",
        },
        {
            "id": "nuts",
            "name": "Nuts",
            "short_description": "Work with screws and bolts to clamp parts tightly.",
        },
        {
            "id": "torque-nuts",
            "name": "Torque / Brake Nuts",
            "short_description": "Special nuts that resist loosening anywhere along the screw.",
        },
    ]

    context = {
        "step1_tools": step1_tools,
        "assembly_items": assembly_items,
    }
    return render(request, "lessons/know_your_tools.html", context)
