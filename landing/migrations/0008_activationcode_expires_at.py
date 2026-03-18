from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("landing", "0007_add_reusable_activation_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="activationcode",
            name="expires_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
