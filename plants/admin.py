from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['scientific_name', 'get_primary_common_name', 'plant_family', 'is_verified']
    list_filter = ['plant_family', 'traditional_systems', 'is_verified']
    search_fields = ['scientific_name', 'common_names']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Botanical Information', {
            'fields': ('common_names', 'scientific_name', 'plant_family', 'description', 'habitat', 'regions')
        }),
        ('Historical Context', {
            'fields': ('traditional_systems', 'cultural_uses', 'parts_used')
        }),
        ('Traditional Knowledge', {
            'fields': ('preparations', 'dosage_info')
        }),
        ('Scientific Research', {
            'fields': ('active_compounds', 'research_studies', 'pharmacological_actions')
        }),
        ('Safety Information', {
            'fields': ('safety_warnings', 'contraindications', 'interactions', 'toxicity_info')
        }),
        ('Conservation', {
            'fields': ('conservation_status', 'sustainability_info', 'ethical_sourcing')
        }),
        ('Media', {
            'fields': ('image_url', 'image_credit')
        }),
        ('Metadata', {
            'fields': ('is_verified', 'created_at', 'updated_at')
        }),
    )
