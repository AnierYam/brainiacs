# AI Coding Agent Instructions - Brainiacs Site

## Project Overview

**Brainiacs Site** is a Django educational platform for teaching robotics (Pedro the robot) through a mission-based learning system. The project organizes content into 4 progressive missions, each with lessons, quizzes, and hands-on activities. The `lessons` Django app contains all view logic, URL routing, and a content-driven architecture (no database models required).

## Architecture & Data Flow

### Mission Structure (Content-First Pattern)

The app uses **in-code dictionaries** instead of database models to define lesson content:

- **Mission 1 (Tools & Fasteners)**: `MISSION1_TOOL_LESSONS` and `MISSION1_FASTENER_LESSONS` dicts in `views.py`
- **Mission 2 (Arduino)**: `MISSION2_PART1_LESSONS` and `MISSION2_PART2_LESSONS` lists
- **Mission 3 (Building Pedro)**: `MISSION3_SYSTEMS` list containing 7 subsystems (body, head, tail, legs, battery, stand), each with nested lessons
- **Mission 4 (Assembly)**: `MISSION4_STEPS` list for final integration steps

### Lesson Dictionary Schema

Each lesson/item follows a consistent pattern:

```python
{
    "slug": "string-identifier",           # URL-safe key for routing
    "title": "Display Title",              # Shown in detail pages
    "name": "Short Name" (optional),       # For list displays
    "type": "tool|fastener|quiz",          # Content category
    "description": "...",                  # Help text
    "part": 1 or 2 (M2 only)              # Mission 2 grouping
}
```

### View Pattern: Lookup & 404

All detail views follow the same pattern:
1. Search lesson dict/list for matching slug
2. Raise `Http404` if not found
3. Pass lesson dict to template

Example from Mission 1:
```python
def _get_mission1_lesson_or_404(slug: str):
    lesson = MISSION1_TOOL_LESSONS.get(slug) or MISSION1_FASTENER_LESSONS.get(slug)
    if not lesson:
        raise Http404("Mission 1 lesson not found")
    return lesson
```

Mission 3 uses nested iteration:
```python
def mission_3_lesson_detail(request, system_slug, lesson_slug):
    system = next((s for s in MISSION3_SYSTEMS if s["slug"] == system_slug), None)
    lesson = next((l for l in system["lessons"] if l["slug"] == lesson_slug), None)
    if not system or not lesson:
        raise Http404(...)
```

## URL Routing Conventions

Each mission has its own URL namespace pattern:

- `/mission-1/` → overview page
- `/mission-1/tool/<slug>/` and `/mission-1/fastener/<slug>/` → detail pages (same template)
- `/mission-1/quiz/part-1/` and `/mission-1/quiz/part-2/` → quiz views (render detail template with synthetic lesson dict)
- `/mission-3/<system_slug>/<lesson_slug>/` → nested routing for systems & lessons
- `/mission-4/<slug>/` → flat routing for final steps

See `urls.py` for all 21 routes.

### URL Aliases
Some routes have multiple names pointing to the same view (e.g., `missions_home` and `lessons_home` both point to `/`). These aliases exist because template names changed or multiple naming conventions were used. Always use the primary name (`missions_home`, `mission_1`, `mission_2_intro`, etc.) in new code; aliases are for backward compatibility with existing templates.

## Template Structure

Templates live in `templates/lessons/`:

- `missions_home.html` - homepage listing all 4 missions
- `mission_1.html` - Mission 1 overview (passes tools + fasteners lists)
- `mission_1_lesson_detail.html` - shared template for tools/fasteners/quizzes
- `mission_2_intro.html` - M2 overview (passes part1/part2 lesson lists)
- `mission_2_lesson_details.html` - M2 lesson detail
- `mission_3_build_pedro.html` - M3 overview (passes systems list)
- `mission_3_lesson_detail.html` - M3 lesson detail (has system + lesson context)
- `mission_4_assemble_pedro.html` - M4 overview (passes steps list)
- `mission_4_step_detail.html` - M4 step detail

Static assets in `static/lessons/`: `fasteners/`, `icons/`, `mission2/`, `tools/` directories hold images and resources.

## Adding New Content

### To add a lesson to Mission 1:
1. Add entry to `MISSION1_TOOL_LESSONS` or `MISSION1_FASTENER_LESSONS` dict with required fields (slug, name, title, type, description)
2. URL routing is automatic based on slug
3. Detail view uses existing `mission_1_lesson_detail()` function

### To add a Mission 2 lesson:
1. Add dict to `MISSION2_PART1_LESSONS` or `MISSION2_PART2_LESSONS` list (requires slug, title, part)
2. Reuse existing `mission_2_lesson_detail()` view - it iterates both lists

### To add a system or lesson to Mission 3:
1. Add system dict to `MISSION3_SYSTEMS` with nested lessons list
2. Each lesson needs slug + title
3. Reuse existing `mission_3_lesson_detail()` view - it handles nested lookup
4. Update `urls.py` pattern if changing system structure (currently `<system_slug>/<lesson_slug>/`)

### To add a Mission 4 step:
1. Add dict to `MISSION4_STEPS` (requires slug + title)
2. Reuse existing `mission_4_step_detail()` view

## Project-Specific Patterns

### 1. No Database Models
`models.py` is intentionally empty. All content is defined in `views.py` dictionaries. This is a **design choice** - content is static, version-controlled, and easier to maintain in the educational context.

### 2. Synthetic Lesson Objects for Quizzes
Quizzes don't have entries in lesson dicts. Instead, `mission_1_part_1_quiz()` and `mission_1_part_2_quiz()` create minimal dicts inline:
```python
{"title": "Mission 1 – Part 1 Quiz (Tools)", "type": "quiz"}
```
This allows reusing the shared detail template without database entries.

### 3. Single vs. Nested Routing
- Missions 1, 2, 4 use flat slugs: `mission-X/<slug>/`
- Mission 3 uses nested: `mission-3/<system_slug>/<lesson_slug>/`
  - Reason: 7 systems × 3 lessons = 21 items. Nesting organizes this hierarchy.

### 4. Slug-Based Lookups (No IDs)
All content is retrieved by `slug`, not ID. Slugs are human-readable, URL-safe identifiers.

## Common Development Tasks

### Adding a new mission (e.g., Mission 5)
1. Create view function(s) in `views.py` following existing mission patterns
2. Add lesson data dict/list following the schema (slug, title, type, description)
3. Add URL patterns to `urls.py` (consider nesting if >5 items)
4. Create templates in `templates/lessons/`
5. Add link in `missions_home.html`

### Updating lesson content
Edit the dict directly in `views.py`. No migrations needed. Example:
```python
MISSION1_TOOL_LESSONS["cross-head-screwdriver"]["description"] = "New description"
```

### Debugging a 404
1. Check slug spelling in URL matches dict key
2. Verify the detail view is searching the correct dict/list
3. Confirm `urls.py` pattern passes correct `<slug>` or `<system_slug>/<lesson_slug>`

### Testing
Create tests in `tests.py` using Django's `TestCase`. The test file is currently empty but follows this pattern:

```python
from django.test import TestCase, Client
from django.urls import reverse

class Mission1Tests(TestCase):
    def test_missions_home_loads(self):
        response = self.client.get(reverse('lessons:missions_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/missions_home.html')

    def test_mission_1_tool_detail(self):
        response = self.client.get(reverse('lessons:mission_1_tool_detail', 
                                          args=['cross-head-screwdriver']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lesson']['slug'], 'cross-head-screwdriver')

    def test_invalid_tool_slug_404(self):
        response = self.client.get(reverse('lessons:mission_1_tool_detail', 
                                          args=['nonexistent-tool']))
        self.assertEqual(response.status_code, 404)

    def test_mission_3_nested_routing(self):
        response = self.client.get(reverse('lessons:mission_3_lesson_detail', 
                                          args=['pedro-body', 'build-structure']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('system', response.context)
        self.assertIn('lesson', response.context)
```

**Test execution** (run from parent Django project directory):
```bash
python manage.py test lessons
python manage.py test lessons.tests.Mission1Tests.test_missions_home_loads  # specific test
python manage.py test lessons -v 2  # verbose output
```

## External Dependencies & Setup

**Django only** - the `lessons` app has minimal dependencies:
- `django.http` (Http404, HttpResponse)
- `django.shortcuts` (render)
- `django.urls` (path routing)
- `django.test` (TestCase, Client)

No third-party packages are used in this app. The parent project (`brainiacs_site`) handles Django configuration (`settings.py`, `manage.py`).

## File Reference Guide

- `views.py` - All view functions & lesson data dicts (~280 lines)
- `urls.py` - URL routing patterns (~70 lines)
- `models.py` - Empty (no database models used)
- `apps.py` - Django app configuration (no customization needed)
- `admin.py` - Empty (no admin registration)
- `templates/lessons/` - HTML templates (9 files)
- `static/lessons/` - Images and static assets

## Key Design Principles

1. **Content as Code**: Lesson data in Python dicts, not database
2. **DRY URL Routing**: Reuse templates for similar content types (e.g., tools & fasteners share template)
3. **Consistent Schemas**: Each lesson type has predictable dict structure
4. **Explicit 404 Handling**: All detail views validate slugs before rendering
5. **Progressive Missions**: Content builds from tools → Arduino → building → assembly

## Future: Database Migration Strategy

The current in-code dictionary approach is intentional for early-stage development. When ready to migrate to a database:

1. **Create Django models** in `models.py`: `Lesson`, `Mission`, `System`, `Step` with appropriate fields (slug, title, description, order, mission_fk, etc.)
2. **Create data migration**: Use `python manage.py makemigrations` and populate with current dict content
3. **Update views**: Replace dict lookups with ORM queries (e.g., `Lesson.objects.get(slug=slug)` instead of dict.get())
4. **Update `urls.py`**: No URL pattern changes needed—routing stays the same
5. **Consider admin interface**: Register models in `admin.py` for content editing
6. **Add caching**: Use Django cache for frequently accessed lessons (dicts currently load on every request, but are fast; DB queries may warrant caching)

This approach maintains the same external API (views, URLs, templates) during migration.
