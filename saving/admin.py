from django.contrib import admin
from .models import SavingTarget, SavingGoal, expectedIncome
# Register your models here.
admin.site.register(SavingTarget)
admin.site.register(SavingGoal)
admin.site.register(expectedIncome)