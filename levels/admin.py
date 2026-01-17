from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Badge, BadgeAward, CodeBlock, Lesson, LessonCard, Level, Quiz, Step, StepCompletion, System


class BrainiacsAdminSite(AdminSite):
    site_header = "Brainiacs Admin"
    site_title = "Brainiacs Admin Portal"
    index_title = "Levels Administration"

    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)

        # Reorder the models manually here
        ordering = {
            "levels": [
                "Level",
                "System",
                "Lesson",
                "LessonCard",
                "Step",
                "StepCompletion",
                "Badge",
                "BadgeAward",
                "Quiz",
                "CodeBlock",
            ]
        }

        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        for app in app_list:
            if app['app_label'] in ordering:
                ordered_models = ordering[app['app_label']]
                app['models'].sort(key=lambda x: ordered_models.index(x['object_name']) if x['object_name'] in ordered_models else 999)
        return app_list


# Replace default admin site with the custom one
class LessonCardInline(admin.TabularInline):
    model = LessonCard
    extra = 0


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonCardInline]


@admin.register(LessonCard)
class LessonCardAdmin(admin.ModelAdmin):
    list_display = ("lesson", "order", "card_type", "title")

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("mission_number", "group_slug", "slug", "title", "content_mode", "is_quiz", "xp_reward", "order")
    list_filter = ("mission_number", "content_mode", "is_quiz")
    search_fields = ("slug", "title", "group_slug")

@admin.register(StepCompletion)
class StepCompletionAdmin(admin.ModelAdmin):
    list_display = ("step", "user", "session_key", "xp_earned", "completed_at")
    list_filter = ("step__mission_number",)
    search_fields = ("step__slug", "user__username", "session_key")

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "mission_number", "rule_type", "rule_value", "xp_threshold")
    list_filter = ("mission_number", "rule_type")
    search_fields = ("name",)

@admin.register(BadgeAward)
class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ("badge", "user", "session_key", "awarded_at")
    list_filter = ("badge__mission_number",)
    search_fields = ("badge__name", "user__username", "session_key")


custom_admin_site = BrainiacsAdminSite(name="custom_admin")

# Register models with custom admin
custom_admin_site.register(Level)
custom_admin_site.register(System)
custom_admin_site.register(Lesson)
custom_admin_site.register(LessonCard)
custom_admin_site.register(Step)
custom_admin_site.register(StepCompletion)
custom_admin_site.register(Badge)
custom_admin_site.register(BadgeAward)
custom_admin_site.register(Quiz)
custom_admin_site.register(CodeBlock)

# Register models with default admin site
admin.site.register(Level)
admin.site.register(System)
admin.site.register(Quiz)
admin.site.register(CodeBlock)
