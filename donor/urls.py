from django.urls import path
from . import views

# Api URLs
urlpatterns = [

    # Endpoint for user registration
    path('register/', views.RegisterAPI.as_view(), name='register'),

    # Endpoint for retrieving donor details
    path('', views.DonorAPI.as_view(), name='donor_detail'),
]
