from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test_page, name="lessons_test"),
    path("know-your-tools/", views.know_your_tools, name="know_your_tools"),
]
