from django.contrib import admin

# Register your models here.
from .models import *
 
class PersonalDetail(admin.ModelAdmin):
   list_display = ('id','name','email')

class AcademicDetail(admin.ModelAdmin):
   list_display = ('id','internprofile_id','marksheet_10','marksheet_12','marksheet_clg')


admin.site.register(InternProfile)
admin.site.register(PersonalDetails,PersonalDetail)
admin.site.register(AcademicDetails,AcademicDetail)
admin.site.register(ProjectDetails)
