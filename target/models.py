from django.db import models
from django.contrib.auth.models import User
from family.models import family

# Create your models here.
class main_category(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255, null=True)    
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
    
class categories_table(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    categories_name = models.CharField(max_length=255, null=True)
    Fixed_fees = models.CharField(default=False)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
    main_category_id = models.ForeignKey(main_category,on_delete=models.CASCADE, null=True, blank=True)



class budget_target(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=255)
    month = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=255, null=True, blank=True)
    category_id = models.ForeignKey(categories_table,on_delete=models.CASCADE)
    target = models.FloatField()
    date = models.DateField(null=True, blank=True)
    family_id = models.ForeignKey(family, on_delete=models.CASCADE, null=True, blank=True)
    
