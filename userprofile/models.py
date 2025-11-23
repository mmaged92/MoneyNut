from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    Address = models.CharField(max_length=255, null=True, blank=True)
    Country = models.CharField(max_length=255, null=True, blank=True)
    Region = models.CharField(max_length=255, null=True, blank=True)
    ZIP_Code = models.CharField(max_length=255, null=True, blank=True)
    Marital_Status = models.CharField(max_length=255, null=True, blank=True)
    Phone_number = models.IntegerField( null=True, blank=True)
    Job_Title = models.CharField(max_length=255, null=True, blank=True)
    Gender = models.CharField(max_length=255, null=True, blank=True)