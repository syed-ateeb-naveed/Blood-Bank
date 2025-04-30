from django.urls import path
from . import views

# Api URLs
urlpatterns = [
    # Endpoint for retrieving donations
    path('donations/', views.DonationListView.as_view(), name='donations'),
]
