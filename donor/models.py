from django.db import models

# Create your models here.

class Donor(models.Model):

    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='donor')
    blood_group = models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)
    # genotype = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    ailments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    
class Donation(models.Model):

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    date = models.DateField()
    time = models.TimeField()
    units = models.IntegerField(default=1)
    location = models.CharField(max_length=255)
