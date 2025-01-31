from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the User model.
    """
    list_display = ['first_name', 'last_name', 'email', 'date_of_birth', 'age']

    search_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'age']

    list_filter = ['created_at', 'modified_at', 'is_active', 'is_staff']

    readonly_fields = ['created_at', 'modified_at']

    ordering = ['-created_at']

    list_per_page = 20