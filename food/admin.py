from django.contrib import admin

from .models import FoodClaim, FoodListing


@admin.register(FoodListing)
class FoodListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'quantity', 'pickup_location', 'latitude', 'longitude', 'status', 'expiry_date')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'pickup_location')


@admin.register(FoodClaim)
class FoodClaimAdmin(admin.ModelAdmin):
    list_display = ('listing', 'receiver', 'created_at')

# Register your models here.
