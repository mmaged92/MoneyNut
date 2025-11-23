from django.contrib import admin
from .models import family, familyMemebers, invitationstatus
# Register your models here.

admin.site.register(family)
admin.site.register(familyMemebers)
admin.site.register(invitationstatus)

