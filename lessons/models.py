from django.conf import settings
from django.db import models


class Badge(models.Model):
    slug = models.SlugField(max_length=100)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    xp_reward = models.PositiveIntegerField(default=0)
    rule_type = models.CharField(max_length=100)
    rule_target = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Step(models.Model):
    CONTENT_CHOICES = [
        ("video", "Video"),
        ("cards", "Cards"),
    ]

    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=255)
    parent_slug = models.SlugField(max_length=100)
    order = models.PositiveIntegerField(default=1)
    content_mode = models.CharField(max_length=10, choices=CONTENT_CHOICES)
    has_quiz = models.BooleanField(default=False)
    youtube_id = models.CharField(max_length=50, blank=True)
    xp_on_complete = models.PositiveIntegerField(default=0)
    xp_on_quiz_correct = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["parent_slug", "order"]
        unique_together = ("slug", "parent_slug")

    def __str__(self):
        return f"{self.parent_slug} - {self.title}"


class StepCompletion(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_step_completions",
    )
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)
    quiz_passed = models.BooleanField(default=False)
    xp_earned = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "step")

    def __str__(self):
        return f"{self.user} - {self.step}"


class StepReview(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reviewed_on = models.DateField(auto_now_add=True)
    xp_awarded = models.PositiveIntegerField(default=5)

    class Meta:
        unique_together = ("step", "user", "reviewed_on")

    def __str__(self):
        return f"{self.user} reviewed {self.step} on {self.reviewed_on}"


class BadgeAward(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_badge_awards",
    )
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "badge")

    def __str__(self):
        return f"{self.user} - {self.badge}"
