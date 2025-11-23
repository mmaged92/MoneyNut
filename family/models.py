from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class family(models.Model):
    Token = models.CharField(max_length=255, null=True,blank=True)
    
    
class invitationstatus(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email_sent = models.CharField(max_length=255, blank=True, null=True)
    invitation_status = models.CharField(max_length=255, blank=True, null=True)

    
class familyMemebers(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
    invitation_id = models.ForeignKey(invitationstatus, on_delete=models.CASCADE, null=True, blank=True)
    

