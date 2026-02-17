from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "landing"

urlpatterns = [
    path('', views.home, name='home'),
    path('demo/', views.demo, name='demo'),
    path('buy/', views.buy, name='buy'),
    path('login/', RedirectView.as_view(url='/auth/login/?next=/lessons/', permanent=False), name='legacy_login'),
    path('activate/', views.activate, name='activate'),
]
