from django.urls import path
from . import views

urlpatterns = [
    path('system/learning-path/', views.learning_path_view, name='learning_path'),
    path('system/<int:pk>/', views.system_detail, name='system_detail'),
]
