from django.urls import path
from . import views

# Api URLs
urlpatterns = [
    # Endpoint for retrieving donations
    path('donations/', views.DonationListView.as_view(), name='donations'),

    # Endpoint for retrieving donations by status
    path('donations/<str:status>/', views.DonationListByStatusView.as_view(), name='donations-by-status'),

]
