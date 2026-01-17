from django.contrib import admin

from .models import Badge, BadgeAward, Step, StepCompletion


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ("parent_slug", "order", "title", "content_mode", "has_quiz", "xp_on_complete")


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "xp_reward", "rule_type", "rule_target")


@admin.register(StepCompletion)
class StepCompletionAdmin(admin.ModelAdmin):
    list_display = ("user", "step", "is_complete", "quiz_passed", "xp_earned", "completed_at")


@admin.register(BadgeAward)
class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "awarded_at")
