from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Plant


def plant_list(request):
    """Display list of all verified plants"""
    query = request.GET.get('q', '')
    plants = Plant.objects.filter(is_verified=True)

    if query:
        plants = plants.filter(
            Q(scientific_name__icontains=query) |
            Q(common_names__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'plants': plants,
        'query': query,
        'total_plants': Plant.objects.filter(is_verified=True).count(),
    }
    return render(request, 'plants/plant_list.html', context)


def plant_detail(request, scientific_name):
    """Display detailed information about a specific plant"""
    plant = get_object_or_404(Plant, scientific_name=scientific_name, is_verified=True)

    context = {
        'plant': plant,
    }
    return render(request, 'plants/plant_detail.html', context)
