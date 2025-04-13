from django.db import models
import datetime

# Create your models here.


class Patient(models.Model):
    
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='patient')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Request(models.Model):

    blood_type =  models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)
    request_date = models.DateField(default=datetime.date.today)
    units_required = models.IntegerField(default=1)
    status = models.CharField(choices=[('pending', 'Pending'), ('fulfilled', 'Fulfilled'), ('cancelled', 'Cancelled')], max_length=10, default='pending')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='requests')

    # def __str__(self):
    #     return f"{self.patient.user.first_name} {self.patient.user.last_name} - {self.blood_type} - {self.units_required} - {self.request_date}"