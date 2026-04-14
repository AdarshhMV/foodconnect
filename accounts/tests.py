from django.test import TestCase
from django.urls import reverse

from .models import User


class AccountFlowTests(TestCase):
    def test_signup_creates_user_with_role(self):
        response = self.client.post(
            reverse('signup'),
            {
                'first_name': 'Dana',
                'last_name': 'Donor',
                'username': 'dana',
                'email': 'dana@example.com',
                'role': 'donor',
                'password1': 'SafePass123!',
                'password2': 'SafePass123!',
            },
        )

        self.assertRedirects(response, reverse('donor_dashboard'))
        self.assertTrue(User.objects.filter(username='dana', role='donor').exists())

    def test_donor_login_redirects_to_donor_dashboard(self):
        User.objects.create_user(username='donor1', password='SafePass123!', role='donor')

        response = self.client.post(
            reverse('login'),
            {'username': 'donor1', 'password': 'SafePass123!'},
        )

        self.assertRedirects(response, reverse('donor_dashboard'))

    def test_receiver_login_redirects_to_receiver_dashboard(self):
        User.objects.create_user(username='receiver1', password='SafePass123!', role='receiver')

        response = self.client.post(
            reverse('login'),
            {'username': 'receiver1', 'password': 'SafePass123!'},
        )

        self.assertRedirects(response, reverse('receiver_dashboard'))

# Create your tests here.
