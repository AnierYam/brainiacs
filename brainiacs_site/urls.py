from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BrainiacsLoginView, BrainiacsLogoutView, signup_view

urlpatterns = [
    path('', include(('landing.urls', 'landing'), namespace='landing')),
    path('auth/login/', BrainiacsLoginView.as_view(), name='login'),
    path('auth/signup/', signup_view, name='signup'),
    path('auth/logout/', BrainiacsLogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('system/', include('systems.urls')),     # your existing app
    path('lessons/', include('lessons.urls')),   # lessons app
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
