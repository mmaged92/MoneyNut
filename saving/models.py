from django.db import models
from django.contrib.auth.models import User
from family.models import family
from accounts.models import Accounts
# Create your models here.
class SavingTarget(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    frequency = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    Saving_target = models.FloatField(null=True, blank=True)
    
class SavingGoal(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    create_date = models.DateField(null=True, blank=True)
    Goal_name = models.CharField(max_length=255, null=True, blank=True)
    Goal = models.FloatField(null=True, blank=True)
    Account = models.ForeignKey(Accounts, on_delete=models.CASCADE,null=True, blank=True )
    
class expectedIncome(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
    month = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    frequency = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    Expected_income = models.FloatField(null=True, blank=True)