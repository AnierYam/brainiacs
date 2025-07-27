from django.apps import AppConfig
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

class LevelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'levels'
    verbose_name = _("Levels Administration")

    def ready(self):
        from .models import Level, System, Lesson, Quiz, CodeBlock

        # Unregister models if already registered
        for model in [Level, System, Lesson, Quiz, CodeBlock]:
            try:
                admin.site.unregister(model)
            except admin.sites.NotRegistered:
                pass

        # Register models in desired order
        admin.site.register(Level)
        admin.site.register(System)
        admin.site.register(Lesson)
        admin.site.register(Quiz)
        admin.site.register(CodeBlock)
