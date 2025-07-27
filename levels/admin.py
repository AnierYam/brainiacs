from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Level, System, Lesson, Quiz, CodeBlock


class BrainiacsAdminSite(AdminSite):
    site_header = "Brainiacs Admin"
    site_title = "Brainiacs Admin Portal"
    index_title = "Levels Administration"

    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)

        # Reorder the models manually here
        ordering = {
            "levels": ["Level", "System", "Lesson", "Quiz", "CodeBlock"]
        }

        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        for app in app_list:
            if app['app_label'] in ordering:
                ordered_models = ordering[app['app_label']]
                app['models'].sort(key=lambda x: ordered_models.index(x['object_name']) if x['object_name'] in ordered_models else 999)
        return app_list


# Replace default admin site with the custom one
custom_admin_site = BrainiacsAdminSite(name='custom_admin')

# Register models with custom admin
custom_admin_site.register(Level)
custom_admin_site.register(System)
custom_admin_site.register(Lesson)
custom_admin_site.register(Quiz)
custom_admin_site.register(CodeBlock)
