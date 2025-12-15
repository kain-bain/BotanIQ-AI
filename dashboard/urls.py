from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('save/<int:plant_id>/', views.save_plant, name='save_plant'),
    path('remove/<int:plant_id>/', views.remove_plant, name='remove_plant'),
    path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),
    path('favorite/<int:plant_id>/', views.toggle_favorite, name='toggle_favorite'),
]
