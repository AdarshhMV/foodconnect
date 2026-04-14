from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    RoleBasedLoginView,
    dashboard_view,
    donor_dashboard_view,
    receiver_dashboard_view,
    signup_view,
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('dashboard/donor/', donor_dashboard_view, name='donor_dashboard'),
    path('dashboard/receiver/', receiver_dashboard_view, name='receiver_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
