from django.urls import path
from . import views

# Api URLs
urlpatterns = [


    # Endpoint for retrieving patient details
    # path('', views.PatientAPI.as_view(), name='patient_detail'),

    # Endpoint for making a request
    path('request/', views.RequestAPI.as_view(), name='request'),

    # Endpoint for retrieving all requests
    path('requests/', views.RequestListAPI.as_view(), name='requests'),
]
