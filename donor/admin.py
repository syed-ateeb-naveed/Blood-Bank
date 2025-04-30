from django.contrib import admin
from .models import Donor, Donation
# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Donor model.
    """
    list_display = ['get_donor_object', 'blood_group', 'get_user_email']

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'

    def get_donor_object(self, obj):
        return obj
    get_donor_object.short_description = 'Donor'

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    
    list_display = ['donor', 'date', 'time', 'units', 'location', 'status']
    # list_filter = ['date', 'location']
    search_fields = ['donor__user__email', 'location']
    ordering = ['-date', '-time']
    list_per_page = 20