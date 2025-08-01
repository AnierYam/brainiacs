from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from levels.views import system_list, system_detail, learning_path
from levels.admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('system/', system_list, name='system_list'),
    path('system/<int:system_id>/', system_detail, name='system_detail'),
    path('learning-path/', learning_path, name='learning_path'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
