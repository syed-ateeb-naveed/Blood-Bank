from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

# Api URLs
urlpatterns = [

    # Endpoint for user registration
    path('register/', views.RegisterAPI.as_view(), name='register'),

    # Endpoint for obtaining a new JWT token pair (access and refresh tokens) upon login
    path('login/', views.LoginAPI.as_view(), name='token_obtain_pair'),

    # Endpoint for refreshing the access token using a valid refresh token
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoint for logging out and blacklisting the JWT token
    path('logout/', views.LogoutAPI.as_view(), name='token_blacklist'),

    # Endpoint for retrieving user details
    path('', views.UserAPI.as_view(), name='user_detail'),
]
