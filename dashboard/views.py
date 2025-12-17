from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import UserCollection, SavedPlant, ResearchNote, UserProfile
from plants.models import Plant
from .forms import UserProfileForm
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    """Main user dashboard - redirects staff to admin dashboard"""
    user = request.user

    # Redirect staff/admin users to admin dashboard
    if user.is_staff:
        return redirect('dashboard:admin_dashboard')

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


@login_required
def profile_settings(request):
    """User profile and account settings"""
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard:profile_settings')
    else:
        form = UserProfileForm(instance=profile)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'dashboard/profile_settings.html', context)


# Admin Dashboard Views
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .forms import PlantForm

@staff_member_required
def admin_dashboard(request):
    """Admin dashboard for content management"""
    from django.db.models import Count, Avg, Q
    from datetime import timedelta
    from django.utils import timezone

    # Time-based filters
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    last_7_days = now - timedelta(days=7)

    # Core Statistics
    total_plants = Plant.objects.count()
    verified_plants = Plant.objects.filter(is_verified=True).count()
    unverified_plants = total_plants - verified_plants
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    total_saved_plants = SavedPlant.objects.count()
    total_collections = UserCollection.objects.count()
    total_research_notes = ResearchNote.objects.count()

    # Activity Statistics (last 30 days)
    new_users_30d = User.objects.filter(date_joined__gte=last_30_days).count()
    new_plants_30d = Plant.objects.filter(created_at__gte=last_30_days).count()
    saved_plants_30d = SavedPlant.objects.filter(date_saved__gte=last_30_days).count()

    # Activity Statistics (last 7 days)
    new_users_7d = User.objects.filter(date_joined__gte=last_7_days).count()
    new_plants_7d = Plant.objects.filter(created_at__gte=last_7_days).count()

    # Plant categories
    plants_by_region = Plant.objects.values('regions').annotate(
        count=Count('id')
    ).exclude(regions__isnull=True).order_by('-count')[:5]

    plants_by_system = Plant.objects.values('traditional_systems').annotate(
        count=Count('id')
    ).exclude(traditional_systems__isnull=True).order_by('-count')[:5]

    # User engagement
    users_with_collections = UserCollection.objects.values('user').distinct().count()
    users_with_saved_plants = SavedPlant.objects.values('user').distinct().count()
    avg_plants_per_user = SavedPlant.objects.count() / max(total_users, 1)

    # System health
    plants_without_description = Plant.objects.filter(
        Q(description__isnull=True) | Q(description='')
    ).count()
    plants_without_uses = Plant.objects.filter(
        Q(cultural_uses__isnull=True) | Q(cultural_uses__exact=[])
    ).count()

    context = {
        # Basic counts
        'total_plants': total_plants,
        'verified_plants': verified_plants,
        'unverified_plants': unverified_plants,
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'total_saved_plants': total_saved_plants,
        'total_collections': total_collections,
        'total_research_notes': total_research_notes,

        # Recent activity
        'new_users_30d': new_users_30d,
        'new_plants_30d': new_plants_30d,
        'saved_plants_30d': saved_plants_30d,
        'new_users_7d': new_users_7d,
        'new_plants_7d': new_plants_7d,

        # Categories
        'plants_by_region': plants_by_region,
        'plants_by_system': plants_by_system,

        # Engagement
        'users_with_collections': users_with_collections,
        'users_with_saved_plants': users_with_saved_plants,
        'avg_plants_per_user': round(avg_plants_per_user, 1),

        # System health
        'plants_without_description': plants_without_description,
        'plants_without_uses': plants_without_uses,

        # Recent items
        'recent_plants': Plant.objects.order_by('-created_at')[:8],
        'recent_users': User.objects.order_by('-date_joined')[:8],
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@staff_member_required
def admin_plants(request):
    """Manage plants in admin dashboard"""
    plants = Plant.objects.all().order_by('-created_at')
    return render(request, 'dashboard/admin_plants.html', {'plants': plants})

@staff_member_required
def admin_add_plant(request):
    """Add new plant via admin dashboard"""
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            plant = form.save()
            messages.success(request, f'Plant "{plant.get_primary_common_name()}" added successfully!')
            return redirect('dashboard:admin_plants')
    else:
        form = PlantForm()
    return render(request, 'dashboard/admin_add_plant.html', {'form': form})

@staff_member_required
def admin_edit_plant(request, plant_id):
    """Edit plant via admin dashboard"""
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = PlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
            messages.success(request, f'Plant "{plant.get_primary_common_name()}" updated successfully!')
            return redirect('dashboard:admin_plants')
    else:
        form = PlantForm(instance=plant)
    return render(request, 'dashboard/admin_edit_plant.html', {'form': form, 'plant': plant})

@staff_member_required
def admin_users(request):
    """Manage users in admin dashboard"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'dashboard/admin_users.html', {'users': users})
