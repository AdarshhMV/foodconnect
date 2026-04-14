from django.urls import path

from .views import claim_listing_view, create_listing_view, delete_listing_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('listings/new/', create_listing_view, name='create_listing'),
    path('listings/<int:pk>/delete/', delete_listing_view, name='delete_listing'),
    path('listings/<int:pk>/claim/', claim_listing_view, name='claim_listing'),
]
