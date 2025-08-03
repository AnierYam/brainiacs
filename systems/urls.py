from django.urls import path
from levels.views import system_list, system_detail, learning_path
from levels.admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', system_list, name='system_list'),
    path('<int:system_id>/', system_detail, name='system_detail'),
    path('learning-path/', learning_path, name='learning_path'),
]
