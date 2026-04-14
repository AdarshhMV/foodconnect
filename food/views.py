from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import FoodClaimForm, FoodListingForm
from .models import FoodClaim, FoodListing
from accounts.views import dashboard_redirect_name


def home_view(request):
    listings = FoodListing.objects.select_related('donor').filter(expiry_date__gt=timezone.now()).order_by('-created_at')
    claim_forms = {}
    if request.user.is_authenticated and getattr(request.user, 'role', None) == 'receiver':
        claim_forms = {listing.id: FoodClaimForm(prefix=f'claim-{listing.id}') for listing in listings if listing.status == FoodListing.AVAILABLE}
    return render(
        request,
        'food/home.html',
        {
            'listings': listings,
            'claim_forms': claim_forms,
        },
    )


@login_required
def create_listing_view(request):
    if not request.user.is_donor():
        return HttpResponseForbidden('Only donors can create food listings.')

    form = FoodListingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        listing = form.save(commit=False)
        listing.donor = request.user
        listing.save()
        messages.success(request, 'Food listing created successfully.')
        return redirect(dashboard_redirect_name(request.user))
    return render(request, 'food/create_listing.html', {'form': form})


@login_required
def delete_listing_view(request, pk):
    listing = get_object_or_404(FoodListing, pk=pk, donor=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted.')
        return redirect(dashboard_redirect_name(request.user))
    return render(request, 'food/delete_listing.html', {'listing': listing})


@login_required
def claim_listing_view(request, pk):
    if not request.user.is_receiver():
        return HttpResponseForbidden('Only receivers can claim food listings.')

    listing = get_object_or_404(FoodListing, pk=pk)
    if listing.donor == request.user:
        messages.error(request, 'You cannot claim your own listing.')
        return redirect('home')
    if listing.status == FoodListing.CLAIMED or hasattr(listing, 'claim'):
        messages.error(request, 'This listing has already been claimed.')
        return redirect('home')
    if listing.expiry_date <= timezone.now():
        messages.error(request, 'This listing has expired.')
        return redirect('home')

    form = FoodClaimForm(request.POST or None, prefix=f'claim-{listing.id}')
    if request.method == 'POST' and form.is_valid():
        claim = form.save(commit=False)
        claim.listing = listing
        claim.receiver = request.user
        claim.save()
        listing.status = FoodListing.CLAIMED
        listing.save(update_fields=['status'])
        messages.success(request, 'Food claimed successfully.')
        return redirect(dashboard_redirect_name(request.user))
    return render(request, 'food/claim_listing.html', {'form': form, 'listing': listing})
