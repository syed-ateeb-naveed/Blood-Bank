from django.urls import path
from . import views

# Api URLs
urlpatterns = [
    # Endpoint for retrieving donations
    path('donations/', views.DonationListView.as_view(), name='donations'),

    # Endpoint for retrieving donations by status
    path('donations/<str:status>/', views.DonationListByStatusView.as_view(), name='donations-by-status'),

    # Endpoint for retrieving requests
    path('requests/', views.RequestListView.as_view(), name='requests'),

    # Endpoint for retrieving requests by status
    path('requests/<str:status>/', views.RequestListByStatusView.as_view(), name='requests-by-status'),

    path('request/<int:pk>/', views.RequestDetailUpdateView.as_view(), name='request-detail'),
    path('donation/<int:pk>/', views.DonationDetailUpdateView.as_view(), name='donation-detail'),

    path('inventory/', views.InventoryView.as_view(), name='inventory'),

]
