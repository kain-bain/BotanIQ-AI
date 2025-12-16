from django.test import TestCase
from django.urls import reverse
from .models import Plant


class PlantModelTest(TestCase):
    def setUp(self):
        self.plant = Plant.objects.create(
            common_names=["Test Plant"],
            scientific_name="Testus plantus",
            plant_family="Testaceae",
            description="A test plant for testing purposes",
            habitat="Test habitat",
            regions=["Test Region"],
            traditional_systems=["Test System"],
            cultural_uses=["Testing"],
            parts_used=["Leaves"],
            preparations=["Tea"],
            dosage_info="Test dosage",
            active_compounds=["Test compound"],
            research_studies=["Test study"],
            pharmacological_actions=["Test action"],
            safety_warnings="Test warning",
            contraindications="Test contraindication",
            interactions="Test interaction",
            toxicity_info="Test toxicity",
            conservation_status="Not endangered",
            sustainability_info="Test sustainability",
            ethical_sourcing="Test sourcing",
            is_verified=True
        )

    def test_plant_creation(self):
        """Test that a plant can be created"""
        self.assertEqual(self.plant.scientific_name, "Testus plantus")
        self.assertEqual(self.plant.plant_family, "Testaceae")
        self.assertTrue(self.plant.is_verified)

    def test_plant_str_method(self):
        """Test the string representation of a plant"""
        self.assertEqual(str(self.plant), "Testus plantus")


class PlantViewTest(TestCase):
    def setUp(self):
        self.plant = Plant.objects.create(
            common_names=["Test Plant"],
            scientific_name="Testus plantus",
            plant_family="Testaceae",
            description="A test plant for testing purposes",
            habitat="Test habitat",
            regions=["Test Region"],
            traditional_systems=["Test System"],
            cultural_uses=["Testing"],
            parts_used=["Leaves"],
            preparations=["Tea"],
            dosage_info="Test dosage",
            active_compounds=["Test compound"],
            research_studies=["Test study"],
            pharmacological_actions=["Test action"],
            safety_warnings="Test warning",
            contraindications="Test contraindication",
            interactions="Test interaction",
            toxicity_info="Test toxicity",
            conservation_status="Not endangered",
            sustainability_info="Test sustainability",
            ethical_sourcing="Test sourcing",
            is_verified=True
        )

    def test_plant_list_view(self):
        """Test that plant list view returns 200"""
        response = self.client.get(reverse('plant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testus plantus")

    def test_plant_detail_view(self):
        """Test that plant detail view returns 200"""
        response = self.client.get(reverse('plant_detail', args=[self.plant.scientific_name]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testus plantus")
