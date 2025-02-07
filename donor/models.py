from django.db import models

# Create your models here.

class Donor(models.Model):

    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='donor')
    blood_group = models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, blank=True, null=True)
    # genotype = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female')])
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    ailments = models.TextField(blank=True, null=True)