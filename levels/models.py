from django.conf import settings
from django.db import models

class Level(models.Model):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    required_xp = models.PositiveIntegerField(default=0)
    badge_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Level {self.number}: {self.title}"

class System(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='systems')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} (Level {self.level.number})"

class Lesson(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_link = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='lessons/images/', blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Lesson: {self.title} (System: {self.system.title})"

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.CharField(max_length=500)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C')])

    def __str__(self):
        return f"Quiz: {self.question[:50]}..."

class CodeBlock(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='code_blocks')
    title = models.CharField(max_length=255)
    code = models.TextField()

    def __str__(self):
        return f"{self.title} (Lesson: {self.lesson.title})"


class LessonCard(models.Model):
    CARD_TYPES = [
        ("intro", "Intro"),
        ("visual", "Visual"),
        ("action", "Action"),
        ("quiz", "Quiz"),
        ("code", "Code"),
        ("reward", "Reward"),
    ]
    QUIZ_CHOICES = [("A", "A"), ("B", "B"), ("C", "C")]

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="cards")
    order = models.PositiveIntegerField()
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    image_url = models.CharField(max_length=500, blank=True)
    youtube_id = models.CharField(max_length=64, blank=True)

    question = models.CharField(max_length=500, blank=True)
    choice_a = models.CharField(max_length=255, blank=True)
    choice_b = models.CharField(max_length=255, blank=True)
    choice_c = models.CharField(max_length=255, blank=True)
    correct_choice = models.CharField(max_length=1, choices=QUIZ_CHOICES, blank=True)
    explanation = models.TextField(blank=True)

    action_label = models.CharField(max_length=255, blank=True)
    action_payload = models.JSONField(blank=True, default=dict)

    starter_code = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("lesson", "order")

    def __str__(self):
        return f"{self.lesson.title} - {self.card_type} {self.order}"


class Step(models.Model):
    CONTENT_CHOICES = [
        ("video", "Video"),
        ("cards", "Cards"),
        ("info", "Info"),
    ]
    MISSION_CHOICES = [
        (1, "Mission 1"),
        (2, "Mission 2"),
        (3, "Mission 3"),
        (4, "Mission 4"),
    ]

    mission_number = models.PositiveSmallIntegerField(choices=MISSION_CHOICES)
    group_slug = models.SlugField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=1)
    content_mode = models.CharField(max_length=16, choices=CONTENT_CHOICES, default="info")
    is_quiz = models.BooleanField(default=False)
    xp_reward = models.PositiveIntegerField(default=10)

    class Meta:
        ordering = ["mission_number", "order"]
        unique_together = ("mission_number", "group_slug", "slug")

    def __str__(self):
        if self.group_slug:
            return f"Mission {self.mission_number}: {self.group_slug} / {self.slug}"
        return f"Mission {self.mission_number}: {self.slug}"


class Badge(models.Model):
    RULE_CHOICES = [
        ("mission_complete", "Mission Complete"),
        ("xp_total", "XP Total"),
        ("step_count", "Step Count"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=255, blank=True)
    mission_number = models.PositiveSmallIntegerField(blank=True, null=True)
    rule_type = models.CharField(max_length=32, choices=RULE_CHOICES, default="mission_complete")
    rule_value = models.PositiveIntegerField(default=0)
    xp_threshold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class StepCompletion(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name="completions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    xp_earned = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (
            ("step", "user"),
            ("step", "session_key"),
        )

    def __str__(self):
        return f"{self.step} completed"


class BadgeAward(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="awards")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ("badge", "user"),
            ("badge", "session_key"),
        )

    def __str__(self):
        return f"{self.badge.name} award"
