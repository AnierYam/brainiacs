from django.urls import path
from . import views

app_name = "lessons"

urlpatterns = [
    # ===== Missions home =====
    path("", views.missions_home, name="missions_home"),
    # alias used in some templates
    path("", views.missions_home, name="lessons_home"),

    # ===== Mission 1 – Know your Toolbox =====
    path("mission-1/", views.mission_1, name="mission_1"),

    # circle detail pages (tools + fasteners + quizzes)
    path(
        "mission-1/tool/<slug:slug>/",
        views.mission_1_lesson_detail,
        name="mission_1_tool_detail",
    ),
    path(
        "mission-1/fastener/<slug:slug>/",
        views.mission_1_lesson_detail,
        name="mission_1_fastener_detail",
    ),
    path(
        "mission-1/quiz/part-1/",
        views.mission_1_part_1_quiz,
        name="mission_1_part_1_quiz",
    ),
    path(
        "mission-1/quiz/part-2/",
        views.mission_1_part_2_quiz,
        name="mission_1_part_2_quiz",
    ),
    path(
        "mission-1/assembly/parts/",
        views.mission_1_assembly_parts,
        name="mission_1_assembly_parts",
    ),
    path(
        "mission-1/assembly/parts/<slug:slug>/",
        views.mission_1_lesson_detail,
        name="mission_1_assembly_detail",
    ),

    # ===== Mission 2 – Introduction to Arduino =====
    path("mission-2/", views.mission_2_intro, name="mission_2_intro"),
    # alias for templates that use 'mission_2_page'
    path("mission-2/", views.mission_2_intro, name="mission_2_page"),
    path(
        "mission-2/<slug:slug>/",
        views.mission_2_lesson_detail,
        name="mission_2_lesson_detail",
    ),

    # ===== Mission 3 – Building Pedro =====
    path("mission-3/", views.mission_3_build_pedro, name="mission_3_build_pedro"),
    # alias for templates that use 'mission_3_page'
    path("mission-3/", views.mission_3_build_pedro, name="mission_3_page"),
    path(
        "mission-3/<slug:system_slug>/<slug:lesson_slug>/",
        views.mission_3_lesson_detail,
        name="mission_3_lesson_detail",
    ),

    # ===== Mission 4 – Assemble Pedro =====
    path("mission-4/", views.mission_4_assemble_pedro, name="mission_4_assemble_pedro"),
    # alias for templates that use 'mission_4_page'
    path("mission-4/", views.mission_4_assemble_pedro, name="mission_4_page"),
    path(
        "mission-4/<slug:slug>/",
        views.mission_4_step_detail,
        name="mission_4_step_detail",
    ),

    # ===== Test / legacy =====
    path("test/", views.lessons_test, name="lessons_test"),
    path("know-your-tools/", views.mission_1, name="know_your_tools"),
]
