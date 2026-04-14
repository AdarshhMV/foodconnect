from django.conf import settings
from django.db import models
from django.utils import timezone


class FoodListing(models.Model):
    AVAILABLE = 'available'
    CLAIMED = 'claimed'
    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (CLAIMED, 'Claimed'),
    ]

    donor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='food_listings',
    )
    title = models.CharField(max_length=150)
    description = models.TextField()
    quantity = models.CharField(max_length=100)
    pickup_location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        return self.status == self.AVAILABLE and self.expiry_date > timezone.now()

    @property
    def has_coordinates(self):
        return self.latitude is not None and self.longitude is not None


class FoodClaim(models.Model):
    listing = models.OneToOneField(FoodListing, on_delete=models.CASCADE, related_name='claim')
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='food_claims',
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.receiver.username} claimed {self.listing.title}'
