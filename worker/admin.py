from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Worker)
admin.site.register(models.Inventory)
admin.site.register(models.Location)
admin.site.register(models.Status)