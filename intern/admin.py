from django.contrib import admin

# Register your models here.
from .models import *
 
admin.site.register(InternProfile)
admin.site.register(PersonalDetails)
admin.site.register(AcademicDetails)

