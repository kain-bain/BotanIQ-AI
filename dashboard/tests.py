from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


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
