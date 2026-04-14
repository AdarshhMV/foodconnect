from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .models import FoodClaim, FoodListing


class FoodFlowTests(TestCase):
    def setUp(self):
        self.donor = User.objects.create_user(
            username='donor1',
            password='SafePass123!',
            role='donor',
        )
        self.receiver = User.objects.create_user(
            username='receiver1',
            password='SafePass123!',
            role='receiver',
        )
        self.listing = FoodListing.objects.create(
            donor=self.donor,
            title='Fresh Sandwiches',
            description='Packaged vegetarian sandwiches',
            quantity='10 packs',
            pickup_location='Community Hall',
            expiry_date=timezone.now() + timedelta(days=1),
        )

    def test_donor_can_create_listing(self):
        self.client.login(username='donor1', password='SafePass123!')
        response = self.client.post(
            reverse('create_listing'),
            {
                'title': 'Fruit Boxes',
                'description': 'Mixed seasonal fruits',
                'quantity': '6 boxes',
                'pickup_location': 'Main Street',
                'expiry_date': (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M'),
            },
        )

        self.assertRedirects(response, reverse('donor_dashboard'))
        self.assertTrue(FoodListing.objects.filter(title='Fruit Boxes').exists())

    def test_receiver_can_claim_listing(self):
        self.client.login(username='receiver1', password='SafePass123!')
        response = self.client.post(
            reverse('claim_listing', args=[self.listing.pk]),
            {'claim-1-message': 'I can pick this up this evening.'},
        )

        self.assertRedirects(response, reverse('receiver_dashboard'))
        self.listing.refresh_from_db()
        self.assertEqual(self.listing.status, FoodListing.CLAIMED)
        self.assertTrue(FoodClaim.objects.filter(listing=self.listing, receiver=self.receiver).exists())

    def test_donor_dashboard_shows_incoming_requests(self):
        FoodClaim.objects.create(
            listing=self.listing,
            receiver=self.receiver,
            message='Please keep this aside for me.',
        )
        self.listing.status = FoodListing.CLAIMED
        self.listing.save(update_fields=['status'])

        self.client.login(username='donor1', password='SafePass123!')
        response = self.client.get(reverse('donor_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/donor_dashboard.html')
        self.assertContains(response, 'Incoming Requests')
        self.assertContains(response, 'Please keep this aside for me.')

    def test_receiver_dashboard_shows_listings(self):
        self.listing.latitude = 12.971600
        self.listing.longitude = 77.594600
        self.listing.save(update_fields=['latitude', 'longitude'])

        self.client.login(username='receiver1', password='SafePass123!')
        response = self.client.get(reverse('receiver_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/receiver_dashboard.html')
        self.assertContains(response, 'All Food Listings')
        self.assertContains(response, 'Fresh Sandwiches')
        self.assertContains(response, 'receiver-listings-map')
        self.assertContains(response, '12.9716')

# Create your tests here.
