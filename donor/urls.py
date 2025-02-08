from django.urls import path
from . import views

# Api URLs
urlpatterns = [

    # Endpoint for user registration
    path('register/', views.RegisterAPI.as_view(), name='register'),

    # Endpoint for retrieving donor details
    path('', views.DonorAPI.as_view(), name='donor_detail'),

    # Endpoint for updating donor details
    path('update/', views.UpdateDonorAPI.as_view(), name='update_donor'),

    # Endpoint for partially updating donor details
    path('partial_update/', views.PartialUpdateDonorAPI.as_view(), name='partial_update_donor'),

    # Endpoint for making a donation
    path('donate/', views.DonationAPI.as_view(), name='donate'),

    # Endpoint for retrieving donations
    path('donations/', views.DonationListAPI.as_view(), name='donations'),
]
