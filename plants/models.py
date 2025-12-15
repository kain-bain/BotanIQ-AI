from django.db import models


class Plant(models.Model):
    """Medicinal plant database model"""

    # Botanical Information
    common_names = models.JSONField(help_text="List of common names")
    scientific_name = models.CharField(max_length=200, unique=True)
    plant_family = models.CharField(max_length=100)

    # Description and Basics
    description = models.TextField()
    habitat = models.CharField(max_length=200, blank=True)
    regions = models.JSONField(default=list, help_text="Geographical regions where found")

    # Historical Context
    traditional_systems = models.JSONField(default=list, help_text="Traditional medicine systems (Ayurveda, TCM, etc.)")

    # Cultural Uses
    cultural_uses = models.JSONField(default=list, help_text="Cultural and historical uses")
    parts_used = models.JSONField(default=list, help_text="Plant parts used medicinally")

    # Preparations
    preparations = models.JSONField(default=list, help_text="Traditional preparation methods")
    dosage_info = models.TextField(blank=True, help_text="Traditional dosage information")

    # Scientific Research
    active_compounds = models.JSONField(default=list, help_text="Known active compounds")
    research_studies = models.JSONField(default=list, help_text="Scientific studies and findings")
    pharmacological_actions = models.JSONField(default=list, help_text="Pharmacological effects")

    # Safety Information
    safety_warnings = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    interactions = models.TextField(blank=True)
    toxicity_info = models.TextField(blank=True)

    # Conservation
    conservation_status = models.CharField(max_length=50, blank=True)
    sustainability_info = models.TextField(blank=True)
    ethical_sourcing = models.TextField(blank=True)

    # Media
    image_url = models.URLField(blank=True, help_text="Plant illustration URL")
    image_credit = models.CharField(max_length=200, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['scientific_name']

    def __str__(self):
        return f"{self.scientific_name} ({', '.join(self.common_names[:2])})"

    def get_primary_common_name(self):
        """Get the first common name for display"""
        return self.common_names[0] if self.common_names else self.scientific_name
