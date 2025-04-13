from django.contrib import admin
from . models import Patient, Request
# Register your models here.


admin.site.register(Patient)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Request model.
    """
    list_display = ['patient', 'blood_type', 'units_required', 'request_date', 'status']
    list_filter = ['blood_type', 'status', 'request_date']

    