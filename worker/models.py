from django.db import models

# Create your models here.


class Worker(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='worker')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
class Inventory(models.Model):
    units_available = models.IntegerField(default=0)

    def __str__(self):
        return f"Inventory - {self.units_available} units available"
    
    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventory"
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name + ' - ' + self.address
    
class Status(models.Model):
    status = models.CharField(
        choices=[
            ('pending', 'Pending'),
            ('fulfilled', 'Fulfilled'),
            ('cancelled', 'Cancelled'),
            ('approved', 'Approved'),
            ('declined', 'Declined'),
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed')
        ],
        max_length=10,
        unique=True
    )

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = "Stauts"
        verbose_name_plural = "Stautses"
