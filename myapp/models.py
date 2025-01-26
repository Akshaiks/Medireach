from django.db import models
from django.utils.timezone import now,localtime

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    def __str__(self):
        return self.username

def get_local_time():
    return localtime(now())


class VideoConsultationRequest(models.Model):
    username = models.CharField(max_length=255)
    request_time = models.DateTimeField(default=get_local_time)
    flag = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.username} - {self.request_time}"
    


class VideoConsultation(models.Model):
    request = models.ForeignKey(VideoConsultationRequest, on_delete=models.CASCADE)
    gmeet_url = models.URLField(max_length=200)
    username = models.CharField(max_length=100)
    request_time = models.DateTimeField()

    def __str__(self):
        return f"Consultation with {self.username} at {self.request_time}"
    


class Prescription(models.Model):
    patient_name = models.CharField(max_length=255)
    disease_name = models.CharField(max_length=255)
    medicine = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient_name}"
    



class sensordata(models.Model):
    username = models.CharField(max_length=255)
    temperature = models.CharField(max_length=255)  
    spo2 = models.CharField(max_length=255)       
    heart_rate = models.CharField(max_length=255)   
    systolic_pressure=models.CharField(max_length=255)
    diastolic_pressure=models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Temperature: {self.temperature}, SPO2: {self.spo2}, Heart Rate: {self.heart_rate}, Time: {self.timestamp}"

