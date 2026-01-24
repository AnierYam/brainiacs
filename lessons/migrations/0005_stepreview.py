from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("lessons", "0004_add_m2_arduino_board_quiz_step"),
    ]

    operations = [
        migrations.CreateModel(
            name="StepReview",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reviewed_on", models.DateField(auto_now_add=True)),
                ("xp_awarded", models.PositiveIntegerField(default=5)),
                (
                    "step",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lessons.step"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "unique_together": {("step", "user", "reviewed_on")},
            },
        ),
    ]
