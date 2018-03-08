from django.contrib import admin

# Register your models here.
from .models import *

class ContactDetailAdmin(admin.ModelAdmin):
	list_display = ('id','company_name','hr_email')

class PostDetailAdmin(admin.ModelAdmin):
	list_display = ('id','domain','technology','numberof_interns','time_duration','stipend','apply_by','typeof_internship','company_id')

class UserPostConnectionAdmin(admin.ModelAdmin):
	list_display = ('id','internprofile_id','company_id','postdetails_id','status')

admin.site.register(CompanyProfile)
admin.site.register(ContactDetails,ContactDetailAdmin)
admin.site.register(PostDetails,PostDetailAdmin)
admin.site.register(UserPostConnection,UserPostConnectionAdmin)
admin.site.register(Messages)