from django.shortcuts import render, get_object_or_404
from .models import System

# List view for all systems
def system_list(request):
    systems = System.objects.all().order_by('order')
    return render(request, 'levels/system_list.html', {'systems': systems})

# Detail view for a single system
def system_detail(request, system_id):
    system = get_object_or_404(System, id=system_id)
    return render(request, 'levels/system_detail.html', {'system': system})

# Visual learning path view (styled grid or layout)
def learning_path(request):
    systems = System.objects.all().order_by('order')
    return render(request, 'levels/learning_path.html', {'systems': systems})
