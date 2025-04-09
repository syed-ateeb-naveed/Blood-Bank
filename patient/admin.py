from django.contrib import admin
from . models import Patient, Request
# Register your models here.


admin.site.register(Patient)
admin.site.register(Request)