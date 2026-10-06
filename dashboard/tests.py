from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from plants.models import Plant
from .models import UserCollection, SavedPlant


class DashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_dashboard_requires_login(self):
        """Test that dashboard requires authentication"""
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_authenticated(self):
        """Test that authenticated users can access dashboard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)


class SavedPlantTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="saveduser",
            password="testpass123"
        )
        self.plant = Plant.objects.create(
            common_names=["Test Herb"],
            scientific_name="Testus herbatus",
            plant_family="Testaceae",
            description="Test medicinal plant",
            regions=["Kenya"],
            traditional_systems=[],
            cultural_uses=[],
            parts_used=[],
            preparations=[],
            active_compounds=[],
            research_studies=[],
            pharmacological_actions=[],
            is_verified=True,
        )
        self.collection = UserCollection.objects.create(
            user=self.user,
            name="Research"
        )
        self.saved = SavedPlant.objects.create(
            user=self.user,
            plant=self.plant,
            collection=self.collection,
        )

    def test_toggle_favorite(self):
        self.assertFalse(self.saved.is_favorite)
        self.saved.toggle_favorite()
        self.saved.refresh_from_db()
        self.assertTrue(self.saved.is_favorite)
        self.saved.toggle_favorite()
        self.saved.refresh_from_db()
        self.assertFalse(self.saved.is_favorite)
