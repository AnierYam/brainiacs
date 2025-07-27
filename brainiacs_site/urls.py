# brainiacs_site/urls.py

from django.contrib import admin
from django.urls import path, include
from levels.admin import custom_admin_site  # Import this

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # Use custom admin site
]
