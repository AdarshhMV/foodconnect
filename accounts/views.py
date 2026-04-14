from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from food.models import FoodClaim, FoodListing

from .forms import SignUpForm, StyledAuthenticationForm


def dashboard_redirect_name(user):
    if user.is_donor():
        return 'donor_dashboard'
    return 'receiver_dashboard'


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect(dashboard_redirect_name(user))
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def dashboard_view(request):
    return redirect(dashboard_redirect_name(request.user))


class RoleBasedLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = StyledAuthenticationForm

    def get_success_url(self):
        return reverse(dashboard_redirect_name(self.request.user))


@login_required
def donor_dashboard_view(request):
    if not request.user.is_donor():
        return redirect('receiver_dashboard')

    context = {
        'my_listings': FoodListing.objects.filter(donor=request.user).order_by('-created_at'),
        'incoming_requests': FoodClaim.objects.filter(listing__donor=request.user).select_related('listing', 'receiver').order_by('-created_at'),
    }
    return render(request, 'accounts/donor_dashboard.html', context)


@login_required
def receiver_dashboard_view(request):
    if not request.user.is_receiver():
        return redirect('donor_dashboard')

    available_listings = FoodListing.objects.select_related('donor').order_by('-created_at')
    listings_map_data = [
        {
            'id': listing.id,
            'title': listing.title,
            'description': listing.description,
            'quantity': listing.quantity,
            'pickup_location': listing.pickup_location,
            'status': listing.get_status_display(),
            'donor': listing.donor.username,
            'latitude': float(listing.latitude),
            'longitude': float(listing.longitude),
            'request_url': reverse('claim_listing', args=[listing.pk]),
        }
        for listing in available_listings
        if listing.has_coordinates
    ]
    context = {
        'available_listings': available_listings,
        'listings_map_data': listings_map_data,
        'my_claims': FoodClaim.objects.filter(receiver=request.user).select_related('listing').order_by('-created_at'),
    }
    return render(request, 'accounts/receiver_dashboard.html', context)
