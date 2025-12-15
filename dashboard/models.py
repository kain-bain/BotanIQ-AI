from django.db import models
from django.contrib.auth.models import User
from plants.models import Plant


class UserCollection(models.Model):
    """User's custom collections for organizing saved plants"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)  # For "My Research Library"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.user.username}'s {self.name}"


class SavedPlant(models.Model):
    """Plants saved by users for their research"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_plants')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='saved_by')
    collection = models.ForeignKey(UserCollection, on_delete=models.CASCADE, related_name='plants')
    notes = models.TextField(blank=True, help_text="Personal research notes")
    date_saved = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'plant']  # One save per user per plant

    def __str__(self):
        return f"{self.user.username} saved {self.plant.scientific_name}"


class ResearchNote(models.Model):
    """Detailed research notes for plants"""
    saved_plant = models.ForeignKey(SavedPlant, on_delete=models.CASCADE, related_name='research_notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note: {self.title} - {self.saved_plant}"
