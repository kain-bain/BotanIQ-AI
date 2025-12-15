from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # User Dashboard
    path('', views.dashboard, name='dashboard'),
    path('save/<int:plant_id>/', views.save_plant, name='save_plant'),
    path('remove/<int:plant_id>/', views.remove_plant, name='remove_plant'),
    path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),
    path('favorite/<int:plant_id>/', views.toggle_favorite, name='toggle_favorite'),

    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/plants/', views.admin_plants, name='admin_plants'),
    path('admin/plants/add/', views.admin_add_plant, name='admin_add_plant'),
    path('admin/plants/<int:plant_id>/edit/', views.admin_edit_plant, name='admin_edit_plant'),
    path('admin/users/', views.admin_users, name='admin_users'),
]
