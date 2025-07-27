from django.db import models

class Level(models.Model):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=255)
    required_xp = models.PositiveIntegerField(default=0)
    badge_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Level {self.number} – {self.title}"

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
