from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import UserCollection, SavedPlant, ResearchNote
from plants.models import Plant


@login_required
def dashboard(request):
    """Main user dashboard"""
    user = request.user

    # Get or create default collection
    default_collection, created = UserCollection.objects.get_or_create(
        user=user,
        is_default=True,
        defaults={'name': 'My Research Library', 'description': 'Your main collection of saved plants'}
    )

    # Get user's collections
    collections = UserCollection.objects.filter(user=user).annotate(
        plant_count=Count('plants')
    ).order_by('-is_default', '-updated_at')

    # Get recent saved plants
    recent_plants = SavedPlant.objects.filter(user=user).select_related(
        'plant', 'collection'
    ).order_by('-date_saved')[:10]

    # Get favorite plants
    favorite_plants = SavedPlant.objects.filter(
        user=user, is_favorite=True
    ).select_related('plant', 'collection')[:6]

    # Statistics
    total_saved = SavedPlant.objects.filter(user=user).count()
    total_collections = collections.count()
    total_notes = ResearchNote.objects.filter(saved_plant__user=user).count()

    context = {
        'collections': collections,
        'recent_plants': recent_plants,
        'favorite_plants': favorite_plants,
        'total_saved': total_saved,
        'total_collections': total_collections,
        'total_notes': total_notes,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def save_plant(request, plant_id):
    """Save a plant to user's default collection"""
    plant = get_object_or_404(Plant, id=plant_id, is_verified=True)

    # Get or create default collection
    collection, created = UserCollection.objects.get_or_create(
        user=request.user,
        is_default=True,
        defaults={'name': 'My Research Library', 'description': 'Your main collection of saved plants'}
    )

    # Save plant if not already saved
    saved_plant, created = SavedPlant.objects.get_or_create(
        user=request.user,
        plant=plant,
        defaults={'collection': collection}
    )

    if created:
        messages.success(request, f'{plant.get_primary_common_name()} added to your research library!')
    else:
        messages.info(request, f'{plant.get_primary_common_name()} is already in your library.')

    return redirect('plants:plant_detail', scientific_name=plant.scientific_name)


@login_required
def remove_plant(request, plant_id):
    """Remove a saved plant"""
    plant = get_object_or_404(Plant, id=plant_id)
    SavedPlant.objects.filter(user=request.user, plant=plant).delete()
    messages.success(request, f'{plant.get_primary_common_name()} removed from your library.')
    return redirect('dashboard:dashboard')


@login_required
def collection_detail(request, collection_id):
    """View plants in a specific collection"""
    collection = get_object_or_404(UserCollection, id=collection_id, user=request.user)
    saved_plants = SavedPlant.objects.filter(
        user=request.user, collection=collection
    ).select_related('plant').order_by('-date_saved')

    context = {
        'collection': collection,
        'saved_plants': saved_plants,
    }
    return render(request, 'dashboard/collection_detail.html', context)


@login_required
def toggle_favorite(request, plant_id):
    """Toggle favorite status of a saved plant"""
    saved_plant = get_object_or_404(SavedPlant, user=request.user, plant_id=plant_id)
    saved_plant.is_favorite = not saved_plant.is_favorite
    saved_plant.save()
    return redirect('dashboard:dashboard')
