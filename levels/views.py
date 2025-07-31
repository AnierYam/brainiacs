from django.shortcuts import render, get_object_or_404
from .models import System

def system_detail(request, system_id):
    systems = System.objects.all()
    selected_system = get_object_or_404(System, id=system_id)
    return render(request, 'system_detail.html', {
        'systems': systems,
        'selected_system': selected_system,
    })
def learning_path(request):
    systems = System.objects.all().order_by('order')
    return render(request, 'learning_path.html', {'systems': systems})
